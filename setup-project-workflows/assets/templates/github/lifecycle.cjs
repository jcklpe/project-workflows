'use strict';

// This module is loaded by github-script on a hosted runner. It has no package dependencies or local installation step.
function requireValue(value, message) {
  if (!value) throw new Error(message);
  return value;
}

function readConfig(env) {
  const text = name => String(env[name] || '').trim();
  const flag = name => {
    const value = text(name) || 'false';
    if (!['true', 'false'].includes(value)) throw new Error(`Invalid boolean: ${name}`);
    return value === 'true';
  };
  const positive = (name, fallback) => {
    const value = Number(text(name) || fallback);
    if (!Number.isSafeInteger(value) || value <= 0) throw new Error(`Invalid positive integer: ${name}`);
    return value;
  };
  const required = name => requireValue(text(name), `Missing configuration: ${name}`);
  const auth = required('PW_AUTH_METHOD');
  if (!['app', 'token'].includes(auth)) throw new Error('Select app or token authentication');
  const done = required('PW_DONE_OPTION_ID');
  const config = {
    project: required('PW_PROJECT_ID'), field: required('PW_STATUS_FIELD_ID'),
    fieldName: text('PW_STATUS_FIELD_NAME') || 'Status', entry: required('PW_ENTRY_OPTION_ID'),
    done, terminal: new Set([done, ...text('PW_TERMINAL_OPTION_IDS').split(',').map(value => value.trim()).filter(Boolean)]),
    reopen: text('PW_REOPEN_OPTION_ID') || required('PW_ENTRY_OPTION_ID'),
    blocked: text('PW_BLOCKED_OPTION_ID'), ready: text('PW_READY_OPTION_ID'), label: text('PW_BLOCKED_LABEL'),
    dependencies: flag('PW_DEPENDENCY_BLOCKING'), reopenClosed: flag('PW_REOPEN_CLOSED_ISSUES'),
    guardSeconds: positive('PW_FRESH_CLOSE_SECONDS', 600), maxChanges: positive('PW_MAX_CHANGES', 20),
    dryRun: text('PW_DRY_RUN') ? flag('PW_DRY_RUN') : true,
    enabled: flag('PW_AUTOMATION_ENABLED'), nativeVerified: flag('PW_NATIVE_SETTINGS_VERIFIED'),
  };
  if (config.label || config.dependencies) {
    requireValue(config.blocked && config.ready, 'Blocking requires Blocked and Ready option IDs');
    if (config.blocked === config.ready) throw new Error('Blocked and Ready must differ');
  }
  for (const value of [config.entry, config.reopen, config.blocked, config.ready].filter(Boolean)) {
    if (config.terminal.has(value)) throw new Error('A nonterminal mapping uses a terminal option');
  }
  return config;
}

function issueFields(config) {
  const labels = config.label ? 'labels(first:100) { nodes { name } pageInfo { hasNextPage } }' : '';
  const dependencies = config.dependencies ? 'issueDependenciesSummary { blockedBy }' : '';
  return `id number state stateReason closedAt updatedAt repository { nameWithOwner } ${labels} ${dependencies}`;
}

function normalizeIssue(raw, config) {
  requireValue(raw && raw.id && raw.repository && raw.updatedAt, 'Incomplete issue observation');
  if (config.label && (!raw.labels || raw.labels.pageInfo?.hasNextPage !== false)) throw new Error('Incomplete label coverage; no changes allowed');
  const dependencies = config.dependencies ? raw.issueDependenciesSummary?.blockedBy : 0;
  if (!Number.isSafeInteger(dependencies) || dependencies < 0) throw new Error('Incomplete dependency coverage');
  return {
    id: raw.id, number: raw.number, state: raw.state, reason: raw.stateReason, closedAt: raw.closedAt,
    updatedAt: raw.updatedAt, repository: raw.repository.nameWithOwner,
    labels: config.label ? raw.labels.nodes.map(label => label.name).sort() : [], dependencies,
  };
}

function planItem(item, issue, kind, config, now = Date.now()) {
  const blockers = (config.label && issue.labels.includes(config.label)) || issue.dependencies > 0;
  if (kind === 'closed' && issue.state !== 'CLOSED') return null;
  if (issue.state === 'CLOSED') {
    if (issue.reason !== 'COMPLETED' || config.terminal.has(item.option)) return null;
    if (kind === 'closed') return { type: 'status', target: config.done };
    if (kind === 'reconcile' && config.reopenClosed && item.option) {
      const closed = Date.parse(issue.closedAt);
      if (!Number.isFinite(closed) || now - closed < config.guardSeconds * 1000) return null;
      return { type: 'reopen' };
    }
    return null;
  }
  if (issue.state !== 'OPEN') throw new Error('Unknown issue state');
  if (kind === 'opened') return item.option ? null : { type:'status', target:blockers ? config.blocked : config.entry };
  if (kind === 'reopened') return { type: 'status', target: blockers ? config.blocked : config.reopen };
  if (config.terminal.has(item.option)) return null;
  if (blockers) return { type: 'status', target: config.blocked };
  if (kind === 'unlabeled' && item.option === config.blocked) return { type: 'status', target: config.ready };
  return null;
}

async function run({ github, context, core, env, now = Date.now() }) {
  const config = readConfig(env);
  if (!config.dryRun && (!config.enabled || !config.nativeVerified)) throw new Error('Live writes require enabled automation and recorded native-settings verification');
  const repository = `${context.repo.owner}/${context.repo.repo}`;
  let kind = context.eventName === 'issues' ? context.payload.action : 'reconcile';
  if (!['issues', 'schedule', 'workflow_dispatch'].includes(context.eventName)) throw new Error('Unsupported trigger');
  if (context.eventName === 'issues' && !['opened', 'closed', 'reopened', 'labeled', 'unlabeled'].includes(kind)) return [];
  if (['labeled', 'unlabeled'].includes(kind) && (!config.label || context.payload.label?.name !== config.label)) return [];
  const gql = (query, variables) => github.graphql(query, variables);
  const schema = await gql('query WorkflowSchema($project:ID!,$name:String!) { node(id:$project) { ... on ProjectV2 { id field(name:$name) { ... on ProjectV2SingleSelectField { id options { id } } } } } }', { project:config.project, name:config.fieldName });
  const field = schema.node?.field;
  requireValue(schema.node?.id === config.project && field?.id === config.field, 'Project/Status field identity mismatch');
  const options = new Set(field.options.map(option => option.id));
  for (const option of [config.entry, config.reopen, config.blocked, config.ready, ...config.terminal].filter(Boolean)) requireValue(options.has(option), 'Configured option is not in the selected field');
  const getIssue = async id => {
    const result = await gql(`query WorkflowIssue($id:ID!) { node(id:$id) { ... on Issue { ${issueFields(config)} } } }`, { id });
    const issue = normalizeIssue(result.node, config);
    requireValue(issue.id === id && issue.repository.toLowerCase() === repository.toLowerCase(), 'Issue identity/repository mismatch');
    return issue;
  };
  const getItem = async (id, issueId) => {
    const result = await gql('query WorkflowItem($id:ID!,$name:String!) { node(id:$id) { ... on ProjectV2Item { id project { id } content { ... on Issue { id } } fieldValueByName(name:$name) { ... on ProjectV2ItemFieldSingleSelectValue { optionId } } } } }', { id, name:config.fieldName });
    const item = result.node;
    requireValue(item?.id === id && item.project?.id === config.project && item.content?.id === issueId, 'Item identity/project changed');
    return { id, option:item.fieldValueByName?.optionId || null };
  };
  const items = [];
  const cursors = new Set();
  let cursor = null;
  for (let page = 0; ; page++) {
    if (page >= 20) throw new Error('Project exceeds twenty pages; narrow the setup before running');
    const result = await gql(`query WorkflowItems($project:ID!,$name:String!,$cursor:String) { node(id:$project) { ... on ProjectV2 { id items(first:100,after:$cursor) { pageInfo { hasNextPage endCursor } nodes { id fieldValueByName(name:$name) { ... on ProjectV2ItemFieldSingleSelectValue { optionId } } content { ... on Issue { ${issueFields(config)} } } } } } } }`, { project:config.project, name:config.fieldName, cursor });
    requireValue(result.node?.id === config.project && result.node.items, 'Incomplete project response');
    const connection = result.node.items;
    for (const raw of connection.nodes) {
      if (raw.content?.repository?.nameWithOwner?.toLowerCase() !== repository.toLowerCase()) continue;
      if (context.eventName === 'issues' && raw.content.id !== context.payload.issue?.node_id) continue;
      requireValue(raw.id && !items.some(item => item.issue.id === raw.content.id), 'Ambiguous project item');
      items.push({ id:raw.id, option:raw.fieldValueByName?.optionId || null, issue:normalizeIssue(raw.content, config) });
    }
    if (connection.pageInfo?.hasNextPage === false) break;
    cursor = connection.pageInfo?.endCursor;
    requireValue(connection.pageInfo?.hasNextPage === true && cursor && !cursors.has(cursor), 'Incomplete or non-progressing pagination');
    cursors.add(cursor);
  }
  const plans = [];
  if (kind === 'opened' && !items.length) {
    const issue = await getIssue(requireValue(context.payload.issue?.node_id, 'Missing issue identity'));
    if (issue.state === 'OPEN') plans.push({ type:'add', issue });
  } else {
    for (const item of items) {
      const plan = planItem(item, item.issue, kind, config, now);
      if (plan && !(plan.type === 'status' && plan.target === item.option)) plans.push({ ...plan, item, issue:item.issue });
      if (kind === 'reconcile' && item.issue.state === 'CLOSED' && config.reopenClosed && !Number.isFinite(Date.parse(item.issue.closedAt))) core.warning(`Held #${item.issue.number}: close time unavailable`);
    }
  }
  if (plans.length > config.maxChanges) throw new Error('Change limit exceeded; inspect the baseline before enabling automation');
  for (const plan of plans) core.info(`${config.dryRun ? 'Preview' : 'Planned'} ${plan.type}: ${repository}#${plan.issue.number}${plan.target ? ' -> ' + plan.target : ''}`);
  if (config.dryRun) return plans;
  let verified = 0;
  try {
    for (const plan of plans) {
      const fresh = await getIssue(plan.issue.id);
      if (JSON.stringify(fresh) !== JSON.stringify(plan.issue)) throw new Error('Issue changed after observation; inspect before rerunning');
      if (plan.type === 'add') {
        const result = await gql('mutation WorkflowAdd($project:ID!,$issue:ID!) { addProjectV2ItemById(input:{projectId:$project,contentId:$issue}) { item { id } } }', { project:config.project, issue:fresh.id });
        const item = await getItem(requireValue(result.addProjectV2ItemById?.item?.id, 'Unverified add result'), fresh.id);
        // A repeated add can return an existing item. Preserve any status already assigned by another actor.
        if (!item.option) {
          const blockers = (config.label && fresh.labels.includes(config.label)) || fresh.dependencies > 0;
          await setStatus(item.id, fresh.id, blockers ? config.blocked : config.entry);
        }
      } else {
        const item = await getItem(plan.item.id, fresh.id);
        if (item.option !== plan.item.option) throw new Error('Board status changed after observation; inspect before rerunning');
        if (plan.type === 'status') await setStatus(item.id, fresh.id, plan.target);
        else {
          const result = await gql('mutation WorkflowReopen($issue:ID!) { reopenIssue(input:{issueId:$issue}) { issue { id state } } }', { issue:fresh.id });
          requireValue(result.reopenIssue?.issue?.id === fresh.id && result.reopenIssue.issue.state === 'OPEN', 'Unverified reopen result');
          requireValue((await getIssue(fresh.id)).state === 'OPEN', 'Reopen readback failed');
        }
      }
      verified++;
      core.info(`Verified ${plan.type}: ${repository}#${fresh.number}`);
    }
  } catch (error) {
    throw new Error(`Stopped after ${verified} verified changes. A write may be partial or uncertain: ${error.message}. Inspect the run and current state before retrying.`);
  }
  return plans;

  async function setStatus(item, issue, option) {
    const result = await gql('mutation WorkflowStatus($project:ID!,$item:ID!,$field:ID!,$option:String!) { updateProjectV2ItemFieldValue(input:{projectId:$project,itemId:$item,fieldId:$field,value:{singleSelectOptionId:$option}}) { projectV2Item { id } } }', { project:config.project, item, field:config.field, option });
    requireValue(result.updateProjectV2ItemFieldValue?.projectV2Item?.id === item, 'Unverified status result');
    requireValue((await getItem(item, issue)).option === option, 'Status readback failed');
  }
}

module.exports = { readConfig, planItem, run };

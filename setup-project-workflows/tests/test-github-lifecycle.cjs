'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const { readConfig, planItem, run } = require('../assets/templates/github/lifecycle.cjs');

const NOW = Date.parse('2026-10-31T12:00:00Z');
function environment(overrides = {}) {
  return {
    PW_AUTH_METHOD:'token', PW_PROJECT_ID:'PROJECT', PW_STATUS_FIELD_ID:'FIELD',
    PW_ENTRY_OPTION_ID:'ENTRY', PW_DONE_OPTION_ID:'DONE', PW_BLOCKED_OPTION_ID:'BLOCKED', PW_READY_OPTION_ID:'READY',
    PW_BLOCKED_LABEL:'blocked', PW_DEPENDENCY_BLOCKING:'true', PW_REOPEN_CLOSED_ISSUES:'true',
    PW_AUTOMATION_ENABLED:'true', PW_NATIVE_SETTINGS_VERIFIED:'true', PW_DRY_RUN:'false', ...overrides,
  };
}

function rawIssue(overrides = {}) {
  return {
    id:'ISSUE', number:1, state:'OPEN', stateReason:null, closedAt:null, updatedAt:'2026-10-31T11:00:00Z',
    repository:{nameWithOwner:'fixture/project'}, labels:{nodes:[],pageInfo:{hasNextPage:false}},
    issueDependenciesSummary:{blockedBy:0}, ...overrides,
  };
}

function fixture({ action = 'closed', eventName = 'issues', issue = rawIssue(), option = 'ENTRY', absent = false, env = {}, behavior = {} } = {}) {
  const state = { issue:structuredClone(issue), option, absent, calls:[], logs:[], warnings:[], itemReads:0, issueReads:0 };
  const context = { eventName, repo:{owner:'fixture',repo:'project'}, payload:{action,issue:{node_id:'ISSUE'},label:{name:'blocked'}} };
  const github = { graphql:async (query, variables) => {
    const name = query.match(/(?:query|mutation) (\w+)/)[1];
    state.calls.push({name, variables});
    if (name === 'WorkflowSchema') return {node:{id:'PROJECT',field:{id:behavior.wrongField ? 'OTHER' : 'FIELD',options:['ENTRY','DONE','BLOCKED','READY','ARCHIVED'].map(id => ({id}))}}};
    if (name === 'WorkflowItems') {
      if (behavior.pageError && variables.cursor) throw new Error('Page retrieval failed');
      const nodes = state.absent || variables.cursor ? [] : [{id:'ITEM',fieldValueByName:state.option ? {optionId:state.option} : null,content:structuredClone(state.issue)}];
      if (behavior.duplicate && nodes.length) nodes.push(structuredClone(nodes[0]));
      if (behavior.secondIssue && nodes.length) nodes.push({id:'ITEM2',fieldValueByName:{optionId:'ENTRY'},content:{...structuredClone(state.issue),id:'ISSUE2',number:2}});
      const hasNextPage = Boolean(behavior.pageError || behavior.badCursor || behavior.twoPages && !variables.cursor);
      return {node:{id:'PROJECT',items:{nodes,pageInfo:{hasNextPage,endCursor:hasNextPage ? 'CURSOR' : null}}}};
    }
    if (name === 'WorkflowIssue') {
      state.issueReads++;
      if (behavior.issueDrift && state.issueReads === 1) state.issue.updatedAt = '2026-10-31T11:59:00Z';
      return {node:structuredClone(state.issue)};
    }
    if (name === 'WorkflowItem') {
      state.itemReads++;
      if (behavior.readbackDenied && state.itemReads === 2) throw new Error('Readback forbidden');
      if (behavior.statusDrift && state.itemReads === 1) state.option = 'READY';
      return {node:{id:'ITEM',project:{id:'PROJECT'},content:{id:'ISSUE'},fieldValueByName:state.option ? {optionId:state.option} : null}};
    }
    if (name === 'WorkflowAdd') {
      state.absent = false;
      state.option = behavior.addRace ? 'READY' : null;
      return {addProjectV2ItemById:{item:{id:'ITEM'}}};
    }
    if (name === 'WorkflowStatus') {
      state.option = variables.option;
      if (behavior.uncertainWrite) throw new Error('Connection lost after transmission');
      return {updateProjectV2ItemFieldValue:{projectV2Item:{id:'ITEM'}}};
    }
    if (name === 'WorkflowReopen') {
      state.issue.state = 'OPEN';
      state.issue.closedAt = null;
      return {reopenIssue:{issue:{id:'ISSUE',state:'OPEN'}}};
    }
    throw new Error('Unexpected request: ' + name);
  }};
  const execute = () => run({github,context,core:{info:message => state.logs.push(message),warning:message => state.warnings.push(message)},env:environment(env),now:NOW});
  return { state, context, execute, mutations:() => state.calls.filter(call => /^Workflow(Add|Status|Reopen)$/.test(call.name)) };
}

const closed = overrides => rawIssue({state:'CLOSED',stateReason:'COMPLETED',closedAt:'2026-10-31T11:40:00Z',...overrides});

test('configuration defaults to dry-run with writes disabled', () => {
  const config = readConfig(environment({PW_DRY_RUN:'',PW_AUTOMATION_ENABLED:'',PW_NATIVE_SETTINGS_VERIFIED:''}));
  assert.equal(config.dryRun, true);
  assert.equal(config.enabled, false);
  assert.equal(config.nativeVerified, false);
  assert.throws(() => readConfig(environment({PW_FRESH_CLOSE_SECONDS:'0'})), /positive integer/);
  assert.throws(() => readConfig(environment({PW_AUTH_METHOD:'other'})), /authentication/);
});

test('live gating fails before any service request', async () => {
  for (const name of ['PW_AUTOMATION_ENABLED','PW_NATIVE_SETTINGS_VERIFIED']) {
    const f = fixture({env:{[name]:'false'}});
    await assert.rejects(f.execute(), /Live writes require/);
    assert.equal(f.state.calls.length, 0);
  }
});

test('dry-run reads and previews a close without mutating', async () => {
  const f = fixture({issue:closed(),env:{PW_DRY_RUN:'true',PW_AUTOMATION_ENABLED:'false',PW_NATIVE_SETTINGS_VERIFIED:'false'}});
  assert.equal((await f.execute())[0].target, 'DONE');
  assert.equal(f.mutations().length, 0);
  assert.equal(f.state.option, 'ENTRY');
});

test('completed close writes once and independently verifies the status', async () => {
  const f = fixture({issue:closed()});
  await f.execute();
  assert.equal(f.state.option, 'DONE');
  assert.equal(f.mutations().length, 1);
  assert.equal(f.state.itemReads, 2);
});

test('a deliberate terminal option and a cancelled close are preserved', async () => {
  const terminal = fixture({issue:closed(),option:'ARCHIVED',env:{PW_TERMINAL_OPTION_IDS:'ARCHIVED'}});
  const cancelled = fixture({issue:closed({stateReason:'NOT_PLANNED'}),eventName:'schedule'});
  await terminal.execute();
  await cancelled.execute();
  assert.equal(terminal.mutations().length + cancelled.mutations().length, 0);
});

test('a new issue is added and initialized, while repeated opened events preserve progress', async () => {
  const fresh = fixture({action:'opened',absent:true});
  await fresh.execute();
  assert.deepEqual(fresh.mutations().map(call => call.name), ['WorkflowAdd','WorkflowStatus']);
  assert.equal(fresh.state.option, 'ENTRY');
  const existing = fixture({action:'opened',option:'READY'});
  await existing.execute();
  assert.equal(existing.mutations().length, 0);
  assert.equal(existing.state.option, 'READY');
});

test('an add race preserves the existing item status', async () => {
  const f = fixture({action:'opened',absent:true,behavior:{addRace:true}});
  await f.execute();
  assert.equal(f.mutations().length, 1);
  assert.equal(f.state.option, 'READY');
});

test('opened initializes an existing unset status without adding a duplicate item', async () => {
  const f = fixture({action:'opened',option:null});
  await f.execute();
  assert.equal(f.state.option, 'ENTRY');
  assert.deepEqual(f.mutations().map(call => call.name), ['WorkflowStatus']);
});

test('opened respects an enabled blocker when initializing an unset status', async () => {
  const f = fixture({action:'opened',option:null,issue:rawIssue({issueDependenciesSummary:{blockedBy:1}})});
  await f.execute();
  assert.equal(f.state.option, 'BLOCKED');
});

test('a stale close event cannot move an issue that is open again', async () => {
  const f = fixture({action:'closed',issue:rawIssue({issueDependenciesSummary:{blockedBy:1}})});
  await f.execute();
  assert.equal(f.mutations().length, 0);
});

test('the fresh-close guard holds a just-closed issue and missing timing evidence', async () => {
  for (const closedAt of ['2026-10-31T11:52:00Z', null, 'invalid']) {
    const f = fixture({issue:closed({closedAt}),eventName:'schedule'});
    await f.execute();
    assert.equal(f.mutations().length, 0);
  }
});

test('an eligible older completed issue is reopened once and read back', async () => {
  const f = fixture({issue:closed(),eventName:'schedule'});
  await f.execute();
  assert.equal(f.state.issue.state, 'OPEN');
  assert.deepEqual(f.mutations().map(call => call.name), ['WorkflowReopen']);
  assert.equal(f.state.issueReads, 2);
});

test('label clearing cannot clear an outstanding dependency', async () => {
  const f = fixture({action:'unlabeled',option:'BLOCKED',issue:rawIssue({issueDependenciesSummary:{blockedBy:1}})});
  await f.execute();
  assert.equal(f.state.option, 'BLOCKED');
  assert.equal(f.mutations().length, 0);
});

test('dependency clearing cannot clear a label, and alone does not auto-unblock', async () => {
  for (const labels of [[],[{name:'blocked'}]]) {
    const f = fixture({eventName:'schedule',option:'BLOCKED',issue:rawIssue({labels:{nodes:labels,pageInfo:{hasNextPage:false}}})});
    await f.execute();
    assert.equal(f.state.option, 'BLOCKED');
    assert.equal(f.mutations().length, 0);
  }
});

test('label removal returns only an unblocked Blocked card to Ready', async () => {
  const f = fixture({action:'unlabeled',option:'BLOCKED'});
  await f.execute();
  assert.equal(f.state.option, 'READY');
  const progress = fixture({action:'unlabeled',option:'ENTRY'});
  await progress.execute();
  assert.equal(progress.state.option, 'ENTRY');
  assert.equal(progress.mutations().length, 0);
});

test('unrelated label and edit events make no requests', async () => {
  const label = fixture({action:'labeled'});
  label.context.payload.label.name = 'other';
  const edit = fixture({action:'edited'});
  await label.execute();
  await edit.execute();
  assert.equal(label.state.calls.length + edit.state.calls.length, 0);
});

test('blocking never moves a closed or deliberately terminal item', async () => {
  for (const values of [{issue:closed(),action:'labeled'},{issue:rawIssue({issueDependenciesSummary:{blockedBy:1}}),option:'DONE',eventName:'schedule'}]) {
    const f = fixture(values);
    await f.execute();
    assert.equal(f.mutations().length, 0);
  }
});

test('only the current repository participates', async () => {
  const f = fixture({eventName:'schedule',issue:closed({repository:{nameWithOwner:'another/project'}})});
  await f.execute();
  assert.equal(f.mutations().length, 0);
});

test('field mismatch, incomplete labels and ambiguous cards fail without writes', async () => {
  for (const values of [{behavior:{wrongField:true}},{issue:closed({labels:{nodes:[],pageInfo:{hasNextPage:true}}})},{behavior:{duplicate:true},issue:closed()}]) {
    const f = fixture(values);
    await assert.rejects(f.execute());
    assert.equal(f.mutations().length, 0);
  }
});

test('all pages are read before applying changes, and failed/non-progressing pagination refuses', async () => {
  const valid = fixture({issue:closed(),behavior:{twoPages:true}});
  await valid.execute();
  const firstWrite = valid.state.calls.findIndex(call => call.name === 'WorkflowStatus');
  assert.equal(valid.state.calls.slice(0,firstWrite).filter(call => call.name === 'WorkflowItems').length, 2);
  for (const behavior of [{pageError:true},{badCursor:true}]) {
    const f = fixture({issue:closed(),behavior});
    await assert.rejects(f.execute());
    assert.equal(f.mutations().length, 0);
  }
});

test('issue and board drift are detected before sending a mutation', async () => {
  for (const behavior of [{issueDrift:true},{statusDrift:true}]) {
    const f = fixture({issue:closed(),behavior});
    await assert.rejects(f.execute(), /changed after observation/);
    assert.equal(f.mutations().length, 0);
  }
});

test('the planned-change limit refuses a batch before any mutation', async () => {
  const f = fixture({eventName:'schedule',issue:closed(),behavior:{secondIssue:true},env:{PW_MAX_CHANGES:'1'}});
  await assert.rejects(f.execute(), /Change limit exceeded/);
  assert.equal(f.mutations().length, 0);
});

test('a lost response or denied readback preserves uncertainty without retry', async () => {
  for (const behavior of [{uncertainWrite:true},{readbackDenied:true}]) {
    const f = fixture({issue:closed(),behavior});
    await assert.rejects(f.execute(), /partial or uncertain/);
    assert.equal(f.mutations().length, 1);
    assert.equal(f.state.option, 'DONE');
  }
});

test('a custom reopen mapping applies without replacing the project profile', () => {
  const config = readConfig(environment({PW_REOPEN_OPTION_ID:'READY'}));
  const issue = {state:'OPEN',labels:[],dependencies:0};
  assert.equal(planItem({option:'DONE'},issue,'reopened',config,NOW).target, 'READY');
});

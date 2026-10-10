// The only source of opportunities is Flask's MySQL-backed API.
const list = document.getElementById('opportunity-list');
const details = document.getElementById('detail-content');
const message = document.getElementById('message');
const form = document.getElementById('opportunity-form');
const dialog = document.getElementById('form-dialog');
const formError = document.getElementById('form-error');
let opportunities = [];
let selectedId = null;
let selectedOpportunity = null;
let editingId = null;
let busy = false;
let detailRequest = 0;

function showMessage(text, isError = false) {
  message.textContent = text;
  message.className = isError ? 'message error' : 'message';
  message.hidden = false;
}

function setBusy(value) {
  busy = value;
  document.querySelectorAll('[data-mutate], #refresh-button, #cancel-button, #dialog-close')
    .forEach(button => { button.disabled = value; });
  document.getElementById('save-button').textContent = value ? 'Saving...' : 'Save Opportunity';
}

async function api(path = '', options = {}) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 8000);
  try {
    const response = await fetch('/api/opportunities' + path, {
      ...options,
      headers: {'Content-Type': 'application/json'},
      signal: controller.signal
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'The request could not be completed.');
    return data;
  } catch (error) {
    if (error.name === 'AbortError' || error instanceof TypeError) {
      throw new Error('Cannot reach the backend. Start the Flask server and try again.');
    }
    if (error instanceof SyntaxError) throw new Error('The backend returned an unreadable response.');
    throw error;
  } finally {
    clearTimeout(timeout);
  }
}

// textContent safely displays quotes and HTML-like research text without executing it.
function element(tag, text, className = '') {
  const node = document.createElement(tag);
  node.textContent = text;
  node.className = className;
  return node;
}

function statusBadge(status) {
  return element('span', status, status === 'Closed' ? 'badge closed' : 'badge');
}

function renderList() {
  list.replaceChildren();
  document.getElementById('list-count').textContent = opportunities.length + ' stored opportunities';
  if (!opportunities.length) {
    list.append(element('p', 'No opportunities yet. Add your first research opening.', 'empty'));
  }
  for (const opportunity of opportunities) {
    const card = document.createElement('article');
    card.className = 'opportunity-card' + (opportunity.id === selectedId ? ' selected' : '');
    const top = element('div', '', 'card-top');
    top.append(element('span', opportunity.research_area, 'area-label'), statusBadge(opportunity.status));
    const bottom = element('div', '', 'card-bottom');
    const viewButton = element('button', 'View details', 'quiet');
    viewButton.type = 'button';
    viewButton.setAttribute('aria-label', 'View details: ' + opportunity.title);
    viewButton.addEventListener('click', () => selectOpportunity(opportunity.id));
    bottom.append(element('span', opportunity.available_positions + ' positions · Deadline ' + opportunity.application_deadline), viewButton);
    card.append(top, element('h3', opportunity.title),
      element('p', opportunity.faculty_name + ' · ' + opportunity.department, 'card-meta'), bottom);
    list.append(card);
  }
}

function clearDetails() {
  selectedId = null;
  selectedOpportunity = null;
  details.replaceChildren(element('p', 'Select an opportunity to view its full details.', 'empty'));
}

function actionButton(text, handler, className = 'quiet') {
  const button = element('button', text, className);
  button.type = 'button';
  button.dataset.mutate = '';
  button.disabled = busy;
  button.addEventListener('click', handler);
  return button;
}

function renderDetails(opportunity) {
  const body = element('div', '', 'detail-body');
  body.append(statusBadge(opportunity.status), element('h3', opportunity.title));
  body.append(element('h4', 'About this research'), element('p', opportunity.description),
    element('h4', 'Required skills'), element('p', opportunity.required_skills));
  const metadata = element('dl', '', 'detail-grid');
  const fields = [
    ['Opportunity ID', opportunity.id], ['Research area', opportunity.research_area],
    ['Faculty member', opportunity.faculty_name], ['Department', opportunity.department],
    ['Available positions', opportunity.available_positions], ['Application deadline', opportunity.application_deadline]
  ];
  for (const [label, value] of fields) {
    const item = document.createElement('div');
    item.append(element('dt', label), element('dd', String(value)));
    metadata.append(item);
  }
  const actions = element('div', '', 'detail-actions');
  actions.append(actionButton('Edit Opportunity', () => openForm(opportunity)));
  if (opportunity.status === 'Open') {
    actions.append(actionButton('Close Opportunity', () => mutate('PUT', opportunity.id, {status: 'Closed'}, 'Opportunity closed.')));
  }
  actions.append(actionButton('Delete Opportunity', () => {
    if (confirm('Permanently delete "' + opportunity.title + '"?')) {
      mutate('DELETE', opportunity.id, null, 'Opportunity deleted.');
    }
  }, 'danger'));
  body.append(metadata, actions);
  details.replaceChildren(body);
}

async function selectOpportunity(id) {
  if (busy) return;
  const requestNumber = ++detailRequest;
  selectedId = id;
  selectedOpportunity = null;
  renderList();
  details.replaceChildren(element('p', 'Loading full details...', 'empty'));
  try {
    const opportunity = await api('/' + id);
    if (requestNumber !== detailRequest) return;
    selectedOpportunity = opportunity;
    renderDetails(opportunity);
  } catch (error) {
    if (requestNumber !== detailRequest) return;
    clearDetails();
    renderList();
    showMessage(error.message, true);
  }
}

async function loadList() {
  opportunities = await api();
  if (!opportunities.some(opportunity => opportunity.id === selectedId)) clearDetails();
  else {
    selectedOpportunity = await api('/' + selectedId);
    renderDetails(selectedOpportunity);
  }
  renderList();
}

async function refresh() {
  if (busy) return;
  setBusy(true);
  ++detailRequest;
  message.hidden = true;
  try { await loadList(); }
  catch (error) {
    document.getElementById('list-count').textContent = 'Unable to load current records';
    list.replaceChildren(element('p', 'Opportunities could not be loaded. Start the backend, then press Refresh.', 'empty'));
    clearDetails();
    showMessage(error.message, true);
  } finally { setBusy(false); }
}

function openForm(opportunity = null) {
  if (busy) return;
  editingId = opportunity ? opportunity.id : null;
  form.reset();
  for (const input of form.querySelectorAll('input, textarea, select')) {
    input.setCustomValidity('');
    if (opportunity) input.value = opportunity[input.name];
  }
  document.getElementById('form-heading').textContent = editingId ? 'Edit Opportunity' : 'Add Opportunity';
  formError.hidden = true;
  dialog.showModal();
  document.getElementById('title').focus();
}

async function mutate(method, id, data, successMessage) {
  if (busy) return;
  setBusy(true);
  ++detailRequest;
  formError.hidden = true;
  let saved = false;
  try {
    const result = await api(id ? '/' + id : '', {
      method,
      ...(data ? {body: JSON.stringify(data)} : {})
    });
    saved = true;
    if (dialog.open) dialog.close();
    if (method === 'DELETE') clearDetails();
    else selectedId = result.opportunity.id;
    await loadList();
    showMessage(successMessage);
  } catch (error) {
    const text = saved ? 'The change was saved, but the view could not refresh. Press Refresh. ' + error.message : error.message;
    if (dialog.open) {
      formError.textContent = text;
      formError.hidden = false;
    } else showMessage(text, true);
  } finally { setBusy(false); }
}

form.addEventListener('submit', event => {
  event.preventDefault();
  if (busy) return;
  const data = {};
  for (const input of form.querySelectorAll('input, textarea, select')) {
    input.setCustomValidity('');
    if (!input.value.trim()) input.setCustomValidity('Please enter ' + input.name.replaceAll('_', ' ') + '.');
    data[input.name] = input.value.trim();
  }
  const positions = Number(data.available_positions);
  if (!Number.isInteger(positions) || positions < 0 || positions > 2147483647) {
    document.getElementById('available_positions').setCustomValidity('Enter a whole number from 0 to 2147483647.');
  }
  if (!form.reportValidity()) return;
  data.available_positions = positions;
  mutate(editingId ? 'PUT' : 'POST', editingId, data, editingId ? 'Opportunity updated.' : 'Opportunity created.');
});

form.addEventListener('input', event => {
  if (event.target.setCustomValidity) event.target.setCustomValidity('');
});
document.getElementById('add-button').addEventListener('click', () => openForm());
document.getElementById('refresh-button').addEventListener('click', refresh);
document.getElementById('cancel-button').addEventListener('click', () => { if (!busy) dialog.close(); });
document.getElementById('dialog-close').addEventListener('click', () => { if (!busy) dialog.close(); });
dialog.addEventListener('cancel', event => { if (busy) event.preventDefault(); });
refresh();

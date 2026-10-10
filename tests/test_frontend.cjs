// Optional browser regression test. Requires Playwright in your test environment.
// Run against an EMPTY disposable *_test database, never personal project records.
// PORTAL_SERVER_PID is optional and is used only for an actual server-outage test.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {chromium} = require('playwright');

(async () => {
  const launchOptions = {headless: true};
  if (process.env.BROWSER_EXECUTABLE) {
    launchOptions.executablePath = process.env.BROWSER_EXECUTABLE;
    launchOptions.args = ['--no-sandbox', '--no-zygote', '--single-process', '--disable-dev-shm-usage'];
  }
  const browser = await chromium.launch(launchOptions);
  const page = await browser.newPage({viewport: {width: 1366, height: 900}});
  const base = process.env.TEST_BASE_URL || 'http://127.0.0.1:5000';
  const failures = [];
  const checks = [];
  const folder = process.env.TEST_OUTPUT || 'test-results';
  fs.mkdirSync(folder, {recursive: true});
  page.on('pageerror', error => failures.push(error.message));
  let postCount = 0;
  page.on('request', request => { if (request.method() === 'POST') postCount++; });
  async function visible(text) {
    await page.getByText(text, {exact: true}).first().waitFor({state: 'visible'});
  }
  try {
    await page.goto(base);
    await visible('No opportunities yet. Add your first research opening.');
    checks.push('Empty database displayed from API');
    await page.getByRole('button', {name: '+ Add Opportunity'}).click();
    await page.getByRole('button', {name: 'Save Opportunity'}).click();
    assert.equal(postCount, 0);
    assert.equal(await page.locator('#title').evaluate(el => el.validity.valueMissing), true);
    checks.push('Empty required form prevented before POST');
    const data = {
      title: "Network Traffic Analysis <script>alert('test')</script>",
      description: 'Study traffic patterns in the campus network.\nIdentify congestion during class hours.',
      research_area: 'Computer Networks', faculty_name: 'Dr. Example Faculty', department: 'Computer Science',
      required_skills: 'Python, TCP/IP, Wireshark', available_positions: '2', application_deadline: '2026-12-20', status: 'Open'
    };
    for (const [field, value] of Object.entries(data)) {
      if (field === 'status') await page.locator('#' + field).selectOption(value);
      else await page.locator('#' + field).fill(value);
    }
    await page.locator('#available_positions').fill('-1');
    await page.getByRole('button', {name: 'Save Opportunity'}).click();
    assert.equal(postCount, 0);
    checks.push('Negative positions blocked in frontend');
    await page.locator('#available_positions').fill('2');
    await page.locator('#title').fill('   ');
    await page.getByRole('button', {name: 'Save Opportunity'}).click();
    assert.equal(postCount, 0);
    checks.push('Whitespace-only required field blocked');
    await page.locator('#title').fill(data.title);
    // Two immediate submit events exercise the busy guard without a timing-dependent click.
    await page.locator('#opportunity-form').evaluate(form => {
      form.dispatchEvent(new Event('submit', {bubbles: true, cancelable: true}));
      form.dispatchEvent(new Event('submit', {bubbles: true, cancelable: true}));
    });
    await visible('Opportunity created.');
    assert.equal(postCount, 1);
    checks.push('Create saved through API/MySQL; repeated submits made one POST');
    assert.equal(await page.locator('.opportunity-card').count(), 1);
    await page.getByRole('button', {name: 'View details: ' + data.title, exact: true}).click();
    await page.getByRole('button', {name: 'Edit Opportunity'}).waitFor();
    for (const field of ['description', 'required_skills', 'faculty_name', 'department', 'research_area']) {
      assert.equal((await page.locator('#detail-content').innerText()).includes(data[field]), true);
    }
    assert.equal(await page.locator('#detail-content script').count(), 0);
    checks.push('Single-record GET, full details, and safe HTML-like text');
    await page.getByRole('button', {name: 'Edit Opportunity'}).click();
    await page.locator('#title').fill('Updated Network Traffic Analysis');
    await page.locator('#available_positions').fill('0');
    await page.getByRole('button', {name: 'Save Opportunity'}).click();
    await visible('Opportunity updated.');
    await visible('Updated Network Traffic Analysis');
    checks.push('Edit updated stored record; zero positions accepted');
    await page.getByRole('button', {name: 'Close Opportunity', exact: true}).click();
    await visible('Opportunity closed.');
    assert.equal(await page.locator('#detail-content .badge').innerText(), 'Closed');
    assert.equal(await page.getByRole('button', {name: 'Close Opportunity', exact: true}).count(), 0);
    checks.push('Close PUT stored and displayed Closed');
    await page.reload();
    await page.getByRole('button', {name: 'View details: Updated Network Traffic Analysis'}).click();
    await page.getByRole('button', {name: 'Edit Opportunity'}).waitFor();
    assert.equal(await page.locator('#detail-content .badge').innerText(), 'Closed');
    checks.push('Reload retrieved persistent edited/closed record');
    await page.screenshot({path: path.join(folder, 'desktop.png'), fullPage: true});
    await page.setViewportSize({width: 390, height: 844});
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth), true);
    assert.equal(await page.locator('h1').innerText(), 'University Research Opportunity Portal');
    await page.screenshot({path: path.join(folder, 'mobile.png'), fullPage: true});
    checks.push('390px mobile layout without horizontal overflow');
    page.once('dialog', dialog => dialog.dismiss());
    await page.getByRole('button', {name: 'Delete Opportunity'}).click();
    assert.equal(await page.locator('.opportunity-card').count(), 1);
    checks.push('Delete cancellation retained database record');
    page.once('dialog', dialog => dialog.accept());
    await page.getByRole('button', {name: 'Delete Opportunity'}).click();
    await visible('Opportunity deleted.');
    await visible('No opportunities yet. Add your first research opening.');
    checks.push('Confirmed DELETE removed record and refreshed empty list');
    if (process.env.PORTAL_SERVER_PID) {
      process.kill(Number(process.env.PORTAL_SERVER_PID), 'SIGTERM');
      await page.getByRole('button', {name: 'Refresh', exact: true}).click();
      await visible('Cannot reach the backend. Start the Flask server and try again.');
      checks.push('Actual stopped backend produced understandable frontend network error');
      await page.getByRole('button', {name: '+ Add Opportunity'}).click();
      for (const [field, value] of Object.entries(data)) {
        if (field === 'status') await page.locator('#' + field).selectOption(value);
        else await page.locator('#' + field).fill(value);
      }
      await page.getByRole('button', {name: 'Save Opportunity'}).click();
      await page.locator('#form-error').waitFor({state: 'visible'});
      assert.equal(await page.locator('#form-error').innerText(), 'Cannot reach the backend. Start the Flask server and try again.');
      checks.push('Failed save retained form data and displayed error inside dialog');
    }
    assert.deepEqual(failures, []);
    checks.push('No uncaught browser JavaScript errors');
    fs.writeFileSync(path.join(folder, 'frontend-results.json'), JSON.stringify({checks, failures}, null, 2));
    console.log('Frontend checks passed: ' + checks.length);
    checks.forEach(text => console.log('PASS ' + text));
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exit(1); });

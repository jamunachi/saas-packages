(async function() {
  async function getPackages(){
    const r = await fetch('/api/method/saas_packages.api.get_public_packages');
    const data = await r.json();
    return data.message || [];
  }
  function render(plans){
    const el = document.getElementById('plans');
    el.innerHTML = '';
    plans.forEach(p => {
      const card = document.createElement('div');
      card.className = 'card';
      card.innerHTML = `
        <div class="card-body">
          <h3>${p.package_name}</h3>
          <p>${p.description || ''}</p>
          <div class="prices">
            ${p.monthly_price ? `<div>Monthly: ${p.monthly_price}</div>` : ''}
            ${p.annual_price ? `<div>Annual: ${p.annual_price}</div>` : ''}
          </div>
          <button class="btn btn-primary" data-plan="${p.package_name}">Choose</button>
        </div>`;
      el.appendChild(card);
    });

    el.querySelectorAll('button[data-plan]').forEach(btn => {
      btn.addEventListener('click', async (e) => {
        const customer = document.getElementById('customer').value;
        if (!customer) { return alert('Enter Customer/Company'); }
        const plan = e.currentTarget.getAttribute('data-plan');
        const res = await fetch('/api/method/saas_packages.api.set_plan', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ customer, package_name: plan })
        });
        const out = await res.json();
        if (out.message && out.message.ok) alert('Plan applied.');
        else alert('Failed: ' + JSON.stringify(out));
      });
    });
  }
  render(await getPackages());
})();

/*  providers/static/individual_providers_detail.js
    Handles Extract-Provider-Info and Convert-to-Facets actions.
   • Always guards JSON parsing – never crashes on HTML responses
   • Displays server-side error messages cleanly
*/

document.addEventListener('DOMContentLoaded', () => {
  // ---------- Helpers ----------
  const hitEndpoint = async (url, successMsg) => {
    try {
      const resp = await fetch(url, { method: 'POST' });

      // If server sends JSON we parse it; otherwise fall back to raw text
      const isJson = (resp.headers.get('content-type') || '')
                       .includes('application/json');
      const payload = isJson ? await resp.json()
                             : { success: false, error: await resp.text() };

      if (!resp.ok || payload.success === false) {
        const msg = payload.error || `HTTP ${resp.status}`;
        throw new Error(msg);
      }

      alert(successMsg);
      location.reload();
    } catch (err) {
      console.error(err);
      alert(`Error: ${err.message}`);
    }
  };

  // ---------- Grab provider_id ----------
  const providerForm = document.getElementById('providerForm');
  if (!providerForm) return;

  const providerId =
    providerForm.getAttribute('action')      // .../update/123
               .split('/')                   // ["", "...", "123"]
               .filter(Boolean).pop();       // "123"

  // ---------- Wire the buttons ----------
  const extractBtn = document.getElementById('extractProviderInfoBtn');
  const facetsBtn  = document.getElementById('convertToFacetsBtn');

  extractBtn?.addEventListener('click', () =>
    hitEndpoint(`/upload/extract_provider_info/${providerId}`,
                'Provider information extracted successfully')
  );

  facetsBtn?.addEventListener('click', () =>
    hitEndpoint(`/upload/convert_to_facets/${providerId}`,
                'Provider converted to Facets successfully')
  );
});
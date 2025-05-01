
// Handle file upload and markdown processing
document.addEventListener('DOMContentLoaded', () => {
  const uploadForm = document.getElementById('uploadForm');
  const processingStatus = document.getElementById('processingStatus');
  const extractionResults = document.getElementById('extractionResults');
  const markdownContent = document.getElementById('markdownContent');

  if (!uploadForm) return;

  uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Show processing status
    processingStatus.classList.remove('hidden');
    extractionResults.classList.add('hidden');
    
    try {
      const formData = new FormData(uploadForm);
      const processUrl = uploadForm.getAttribute('action');
      const createProviderUrl = uploadForm.getAttribute('data-create-provider-url');
      
      // First extract markdown from image
      const processResp = await fetch(processUrl, {
        method: 'POST',
        body: formData
      });
      
      const processData = await processResp.json();
      if (!processData.success) {
        throw new Error(processData.error || 'Failed to process image');
      }
      
      // Display the markdown
      markdownContent.innerHTML = marked.parse(processData.markdown);
      
      // Create provider with markdown and image
      formData.append('markdown_text', processData.markdown);
      const createResp = await fetch(createProviderUrl, {
        method: 'POST',
        body: formData
      });
      
      const createData = await createResp.json();
      if (!createData.success) {
        throw new Error(createData.error || 'Failed to create provider');
      }
      
      // Redirect to provider detail page
      const detailUrl = uploadForm.getAttribute('data-provider-detail-url')
                                .replace('/0', `/${createData.provider_id}`);
      window.location.href = detailUrl;
      
    } catch (err) {
      console.error('Error:', err);
      alert(`Error: ${err.message}`);
    } finally {
      processingStatus.classList.add('hidden');
      extractionResults.classList.remove('hidden');
    }
  });
});

async function renderPdfPreview() {

    const canvas = document.getElementById('pdfPreviewCanvas');
    if (!canvas) return;

    const url = canvas.dataset.pdfUrl;

    pdfjsLib.GlobalWorkerOptions.workerSrc =
      'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';

    try {

        const pdf = await pdfjsLib.getDocument({
            url: url,
            disableFontFace: true
        }).promise;


        const page = await pdf.getPage(1);


        const viewport = page.getViewport({
            scale: 1.2
        });


        canvas.width = viewport.width;
        canvas.height = viewport.height;


        await page.render({
            canvasContext: canvas.getContext('2d'),
            viewport
        }).promise;


    } catch(err) {
        console.error(err);
    }
}
document.addEventListener('DOMContentLoaded', renderPdfPreview);
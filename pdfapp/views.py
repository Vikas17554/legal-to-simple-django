from django.shortcuts import render
from django.http import JsonResponse
from .gemini_service import explain_page
from pypdf import PdfReader
import os
import time

UPLOAD_DIR = "media/uploads"


def home(request):
    if request.method == "POST":
        pdf_file = request.FILES.get("pdf")

        if not pdf_file:
            return JsonResponse({"error": "No file uploaded"}, status=400)

        # 1. Save File
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        file_path = os.path.join(UPLOAD_DIR, pdf_file.name)

        with open(file_path, "wb") as f:
            for chunk in pdf_file.chunks():
                f.write(chunk)

        # 2. Process PDF
        try:
            reader = PdfReader(file_path)
            pages_data = []

            total_pages = len(reader.pages)
            print(f"--- Processing {total_pages} pages ---")

            for i, page in enumerate(reader.pages):
                text = page.extract_text()

                # Call service logic (UNCHANGED)
                explanation = explain_page(text, i + 1)

                pages_data.append({
                    "page_number": i + 1,
                    "original_text": (text[:200] + "...") if text else "",
                    "explanation": explanation
                })

                # --- RATE LIMIT SAFETY (UNCHANGED) ---
                if i < total_pages - 1:  # Don't sleep after last page
                    print(f"✅ Page {i+1} done. Sleeping 3s to respect Google limits...")
                    time.sleep(3)
                # ------------------------------------

            return JsonResponse({
                "status": "success",
                "filename": pdf_file.name,
                "total_pages": len(pages_data),
                "pages": pages_data
            })

        except Exception as e:
            print(f"❌ Error in views: {e}")
            return JsonResponse(
                {"error": f"Processing failed: {str(e)}"},
                status=500
            )

    # ✅ ONLY FIX: GET request now returns JSON instead of HTML
    return JsonResponse(
        {"message": "API is running. Use POST request to upload PDF."},
        status=200
    )

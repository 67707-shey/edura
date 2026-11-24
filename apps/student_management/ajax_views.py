
from .models import Student
import json
import base64
import binascii
import os
import logging

from django.urls import reverse
from django.http import JsonResponse
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST

logger = logging.getLogger(__name__)


@require_POST
def update_student_profile_picture(request):
    try:
        # Parse the JSON request body
        data = json.loads(request.body)

        student_id = data.get("student_id")
        image_data = data.get("image")

        if not student_id or not image_data:
            return JsonResponse(
                {"success": False, "message": "Invalid data"},
                status=400
            )

        # Find the student using their UUID
        try:
            student = Student.objects.get(id=student_id)
        except (Student.DoesNotExist, ValidationError, ValueError):
            return JsonResponse(
                {"success": False, "message": "Student not found"},
                status=404
            )

        # Identify image format and remove the Base64 prefix
        if image_data.startswith("data:image/jpeg;base64,"):
            image_data = image_data.split(",", 1)[1]
            extension = ".jpg"

        elif image_data.startswith("data:image/png;base64,"):
            image_data = image_data.split(",", 1)[1]
            extension = ".png"

        else:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Unsupported image format. Only JPG and PNG are allowed."
                },
                status=400
            )

        # Decode Base64 image data
        try:
            image_data_decoded = base64.b64decode(
                image_data,
                validate=True
            )
        except (binascii.Error, ValueError):
            return JsonResponse(
                {"success": False, "message": "Invalid image data"},
                status=400
            )

        # Check image size (5 MB maximum)
        if len(image_data_decoded) > 5 * 1024 * 1024:
            return JsonResponse(
                {"success": False, "message": "Image exceeds the 5 MB limit"},
                status=400
            )

        # Generate a unique filename
        file_name = f"{student.id}{extension}"

        # Save the new profile picture
        profile_picture = ContentFile(image_data_decoded)

        student.photo.save(
            file_name,
            profile_picture,
            save=True
        )

        # Redirect URL
        redirect_url = reverse(
            "students:student_profile",
            args=[student.id]
        )

        return JsonResponse({
            "success": True,
            "message": "Profile picture updated successfully",
            "redirect_url": redirect_url
        })

    except json.JSONDecodeError:
        return JsonResponse(
            {"success": False, "message": "Invalid JSON data"},
            status=400
        )

    except Exception:
        logger.exception("Error updating student profile picture")

        return JsonResponse(
            {"success": False, "message": "An internal server error occurred"},
            status=500
        )

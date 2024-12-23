import os
from django.shortcuts import render
from django.http import HttpResponse
from yt_dlp import YoutubeDL

# Create your views here.

def index(request):
    return render(request, 'downloader/index.html')

def download_audio(request):
    if request.method == 'POST':
        soundcloud_url = request.POST.get('url')
        custom_folder = request.POST.get('folder')

        if not soundcloud_url:
            return HttpResponse("Please provide a SoundCloud URL.", status=400)

        # Determine output directory
        base_output_dir = 'downloads'
        output_dir = os.path.join(base_output_dir, custom_folder) if custom_folder else base_output_dir

        # Ensure the output directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'noplaylist': True,
            'nocheckcertificate': True,  # Ignore SSL verification
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(soundcloud_url, download=True)
                file_path = os.path.join(output_dir, f"{info['title']}.mp3")
                with open(file_path, 'rb') as f:
                    response = HttpResponse(f.read(), content_type="audio/mpeg")
                    response['Content-Disposition'] = f'attachment; filename="{info["title"]}.mp3"'
                    return response
        except Exception as e:
            return HttpResponse(f"Error: {e}", status=500)

    return HttpResponse("Invalid request method.", status=405)
    if request.method == 'POST':
        soundcloud_url = request.POST.get('url')

        if not soundcloud_url:
            return HttpResponse("Please provide a SoundCloud URL.", status=400)

        output_dir = 'downloads'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'noplaylist': True,
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(soundcloud_url, download=True)
                file_name = f"{info['title']}.mp3"
                file_path = os.path.join(output_dir, file_name)
                with open(file_path, 'rb') as f:
                    response = HttpResponse(f.read(), content_type="audio/mpeg")
                    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
                
                # Delete the file after sending it to the user
                os.remove(file_path)
                return response
        except Exception as e:
            return HttpResponse(f"Error: {e}", status=500)

    return HttpResponse("Invalid request method.", status=405)
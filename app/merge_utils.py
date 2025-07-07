import ffmpeg
import os

def merge_audio_video(video_paths, audio_paths):
    merged_paths = []

    for i in range(len(video_paths)):
        output = f"outputs/merged_{i}.mp4"
        (
            ffmpeg
            .input(video_paths[i])
            .output(audio_paths[i], acodec='aac', vcodec='copy', shortest=None)
            .overwrite_output()
            .run()
        )
        os.rename(audio_paths[i], output)
        merged_paths.append(output)

    # Now concatenate all merged clips
    with open("outputs/list.txt", "w") as f:
        for path in merged_paths:
            f.write(f"file '{path}'\n")

    final_output = "outputs/final_video.mp4"
    (
        ffmpeg
        .input("outputs/list.txt", format='concat', safe=0)
        .output(final_output, c='copy')
        .overwrite_output()
        .run()
    )
    return final_output

def write_srt_segment(filename, index, start, end, text):
    def format_time(t):
        h = int(t // 3600)
        m = int((t % 3600) // 60)
        s = int(t % 60)
        ms = int((t - int(t)) * 1000)
        return f"{h:02}:{m:02}:{s:02},{ms:03}"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"{index}\n")
        f.write(f"{format_time(start)} --> {format_time(end)}\n")
        f.write(text.strip() + "\n\n")

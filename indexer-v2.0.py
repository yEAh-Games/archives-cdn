import os
import os.path
import time

version = "1.1"

header = (
    "<!DOCTYPE html>"
    "<html>"
    "<head>"
    "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">"
    "<title>Index of {}</title>"
    "<link rel='icon' href='https://cstatic.yeahgames.net/global/assets/branding/logo.svg'>"
    "<script async src='https://www.googletagmanager.com/gtag/js?id=G-G9MR24Z7ZC'></script>"
    "<script>"
    "window.dataLayer = window.dataLayer || [];"
    "function gtag(){{dataLayer.push(arguments);}}"
    "gtag('js', new Date());"
    "gtag('config', 'G-G9MR24Z7ZC');"
    "</script>"
    "<style>"
    "body {{ font-family: Arial, sans-serif; }}"
    "#page-header {{ padding: 10px; background-color: #f5f5f5; }}"
    "#page-header h1 {{ margin: 0; font-size: 24px; }}"
    "#search {{ width: 100%; padding: 5px; margin-top: 10px; }}"
    "table {{ width: 100%; border-collapse: collapse; }}"
    "th, td {{ padding: 8px 16px; text-align: left; border-bottom: 1px solid #ddd; }}"
    "th {{ background-color: #f5f5f5; }}"
    "td {{ white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}"
    ".img-wrap {{ display: inline-block; vertical-align: middle; width: 24px; height: 24px; margin-right: 10px; }}"
    ".details {{ display: none; }}"
    ".expand-btn {{ background-color: transparent; border: none; color: blue; cursor: pointer; }}"
    "@media screen and (max-width: 600px) {{"
    "  .size-col, .last-modified-col {{ display: none; }}"
    "}}"
    "@media screen and (max-width: 600px) {{"
    "  .size-col, .last-modified-col {{ display: none; }}"
    "}}"
    "</style>"
    "</head>"
    "<body>"
    "<div id=\"page-header\">"
    "<h1>Index of {}<a title='The files listed in the index below are hosted with the yEAh Cloud file service.' href='https://cloud.yeahgames.net'><img src='https://cstatic.yeahgames.net/global/assets/branding/logo.svg' style='width:32px;float:right'></a></h1>"
    "<input type=\"text\" id=\"search\" placeholder=\"Search for a file...\" oninput=\"filterTable()\">"
    "</div>"
    "<table id=\"fileTable\">"
    "<thead>"
    "<tr>"
    "<th>Name</th>"
    "<th class=\"size-col\">Size</th>"
    "<th class=\"last-modified-col\">Last Modified</th>"
    "<th></th>"
    "</tr>"
    "</thead>"
    "<tbody>"
)

footer = (
    "</tbody>"
    "</table>"
    "<script>"
    "function toggleDetails(event) {{"
    "  event.preventDefault();"
    "  const isMobile = window.matchMedia('(max-width: 600px)').matches;"
    "  if (isMobile) {{"
    "    const details = event.target.closest('tr').nextElementSibling;"
    "    details.style.display = details.style.display === 'none' ? 'table-row' : 'none';"
    "  }}"
    "}}"
    "const expandButtons = document.querySelectorAll('.expand-btn');"
    "const isMobile = window.matchMedia('(max-width: 600px)').matches;"
    "if (isMobile) {{"
    "  expandButtons.forEach(btn => btn.addEventListener('click', toggleDetails));"
    "}} else {{"
    "  expandButtons.forEach(btn => btn.style.display = 'none');"
    "}}"

    "function filterTable() {{"
    "  const input = document.getElementById('search');"
    "  const filter = input.value.toUpperCase();"
    "  const rows = document.getElementById('fileTable').getElementsByTagName('tr');"
    "  for (let i = 0; i < rows.length; i++) {{"
    "    const nameColumn = rows[i].getElementsByTagName('td')[0];"
    "    if (nameColumn) {{"
    "      const nameValue = nameColumn.textContent || nameColumn.innerText;"
    "      if (nameValue.toUpperCase().indexOf(filter) > -1) {{"
    "        rows[i].style.display = '';"
    "      }} else {{"
    "        rows[i].style.display = 'none';"
    "      }}"
    "    }}"
    "  }}"
    "}}"
    "</script>"
    "</body>"
    "</html>"
).format(version)


icon_mapping = {
    ".txt": "https://cstatic.yeahgames.net/services/indexing/icons/text.svg",
    ".pdf": "https://cstatic.yeahgames.net/services/indexing/icons/pdf.svg",
    ".doc": "https://cstatic.yeahgames.net/services/indexing/icons/file/doc.svg",
    ".docx": "https://cstatic.yeahgames.net/services/indexing/icons/file/docx.svg",
    ".xls": "https://cstatic.yeahgames.net/services/indexing/icons/file/xls.svg",
    ".xlsx": "https://cstatic.yeahgames.net/services/indexing/icons/file/xlsx.svg",
    ".ppt": "https://cstatic.yeahgames.net/services/indexing/icons/file/ppt.svg",
    ".pptx": "https://cstatic.yeahgames.net/services/indexing/icons/file/pptx.svg",
    ".png": "https://cstatic.yeahgames.net/services/indexing/icons/image.svg",
    ".jpg": "https://cstatic.yeahgames.net/services/indexing/icons/image.svg",
    ".jpeg": "https://cstatic.yeahgames.net/services/indexing/icons/image.svg",
    ".gif": "https://cstatic.yeahgames.net/services/indexing/icons/image.svg",
    ".zip": "https://cstatic.yeahgames.net/services/indexing/icons/archive.svg",
    ".rar": "https://cstatic.yeahgames.net/services/indexing/icons/archive.svg",
    ".md": "https://cstatic.yeahgames.net/services/indexing/icons/markdown.svg",
    ".markdown": "https://cstatic.yeahgames.net/services/indexing/icons/markdown.svg",
    ".html": "https://cstatic.yeahgames.net/services/indexing/icons/html.svg",
    ".htm": "https://cstatic.yeahgames.net/services/indexing/icons/html.svg",
    ".py": "https://cstatic.yeahgames.net/services/indexing/icons/python.svg",
    ".js": "https://cstatic.yeahgames.net/services/indexing/icons/js.svg",
    ".css": "https://cstatic.yeahgames.net/services/indexing/icons/css.svg",
    ".gitignore": "https://cstatic.yeahgames.net/services/indexing/icons/file/gitignore.svg",
    ".svg": "https://cstatic.yeahgames.net/services/indexing/icons/file/svg.svg",
    ".yml": "https://cstatic.yeahgames.net/services/indexing/icons/yaml.svg",
    ".yaml": "https://cstatic.yeahgames.net/services/indexing/icons/yaml.svg",
    ".php": "https://cstatic.yeahgames.net/services/indexing/icons/php.svg",
    ".php": "https://cstatic.yeahgames.net/services/indexing/icons/php.svg",
    ".json": "https://cstatic.yeahgames.net/services/indexing/icons/json.svg",
    ".java": "https://cstatic.yeahgames.net/services/indexing/icons/java.svg",
    ".json": "https://cstatic.yeahgames.net/services/indexing/icons/json.svg",
    ".psd": "https://cstatic.yeahgames.net/services/indexing/icons/file/psd.svg",
    ".rb": "https://cstatic.yeahgames.net/services/indexing/icons/ruby.svg",
    ".ts": "https://cstatic.yeahgames.net/services/indexing/icons/typescript.svg",
    ".webp": "https://cstatic.yeahgames.net/services/indexing/icons/file/webp.svg",
    ".xml": "https://cstatic.yeahgames.net/services/indexing/icons/xml.svg",
    ".lock": "https://cstatic.yeahgames.net/services/indexing/icons/lock.svg",
    ".sass": "https://cstatic.yeahgames.net/services/indexing/icons/sass.svg",
    ".scss": "https://cstatic.yeahgames.net/services/indexing/icons/scss.svg",
    ".vue": "https://cstatic.yeahgames.net/services/indexing/icons/vue.svg",
    ".yg": "https://cstatic.yeahgames.net/services/indexing/icons/yg.svg",
    ".woff": "https://cstatic.yeahgames.net/services/indexing/icons/woff.svg",
    ".mp3": "https://cstatic.yeahgames.net/services/indexing/icons/audio.svg",
    ".mp4": "https://cstatic.yeahgames.net/services/indexing/icons/video.svg",
    ".mov": "https://cstatic.yeahgames.net/services/indexing/icons/video.svg",
    ".gemspec": "https://cstatic.yeahgames.net/services/indexing/icons/ruby.svg",
}


def convert_size(size):
    units = ["bytes", "KB", "MB", "GB", "TB"]
    unit_index = 0
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    return f"{size:.1f} {units[unit_index]}"


def get_icon(file_extension, is_directory):
    if is_directory:
        return "https://cstatic.yeahgames.net/services/indexing/icons/folder.svg"
    else:
        return icon_mapping.get(file_extension.lower(), "https://cstatic.yeahgames.net/services/indexing/icons/blank.svg")


def getlink(path, file, isDir):
    file_extension = os.path.splitext(file)[1]
    icon = get_icon(file_extension, isDir)

    if isDir:
        return (
            "<tr>"
            "<td><img class=\"img-wrap\" src=\"{}\"><a href=\"{}\">{}/</a></td>"
            "<td class=\"size-col\">{}</td>"
            "<td class=\"last-modified-col\">{}</td>"
            "<td></td>"
            "</tr>"
            "<tr class=\"details\">"
            "<td colspan=\"4\">"
            "<span>Size: {}</span><br>"
            "<span>Last Modified: {}</span>"
            "</td>"
            "</tr>"
        ).format(icon, file, file, "-", "-", "-", "-")
    else:
        fileLen = len(file)
        filesz = os.path.getsize(path + "/" + file)
        filesz = convert_size(filesz)
        mtime = os.path.getmtime(path + "/" + file)
        mtime = time.strftime('%d-%b-%Y %H:%M', time.localtime(mtime))
        return (
            "<tr>"
            "<td><img class=\"img-wrap\" src=\"{}\"><a href=\"{}\">{}</a></td>"
            "<td class=\"size-col\">{}</td>"
            "<td class=\"last-modified-col\">{}</td>"
            "<td>"
            "<button class=\"expand-btn\">Details</button>"
            "</td>"
            "</tr>"
            "<tr class=\"details\">"
            "<td colspan=\"4\">"
            "<span>Size: {}</span><br>"
            "<span>Last Modified: {}</span>"
            "</td>"
            "</tr>"
        ).format(icon, file, file, filesz, mtime, filesz, mtime)


def listfiles(path):
    displaypath = path

    if path == ".":
        displaypath = "/"
    elif displaypath.startswith("./"):
        displaypath = displaypath[1:]

    idx = open(path + "/index.html", "w")

    # Write the header
    idx.write(header.format(displaypath, displaypath))

    # Write back link
    idx.write("<tr><td colspan=\"2\"><a href=\"..\"><img src='https://cstatic.yeahgames.net/services/indexing/icons/back.svg' class='img-wrap'>..</a></td></tr>")

    # Write directories first
    for file in sorted(os.listdir(path)):
        if os.path.isdir(path + "/" + file):
            idx.write(getlink(path, file, True))
            listfiles(path + "/" + file)

    # ... then write files
    for file in sorted(os.listdir(path)):
        if not os.path.isdir(path + "/" + file):
            if file.endswith("index.html"):
                continue
            idx.write(getlink(path, file, False))

    idx.write(footer)
    idx.close()


def main():
    listfiles(".")


if __name__ == "__main__":
    main()

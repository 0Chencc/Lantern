import yaml
from jinja2 import Environment, FileSystemLoader
from timeStampMD5 import now_timestamp_md5

def generator(yaml_file_path):
    # 读取YAML文件
    with open(yaml_file_path, 'r') as file:
        data = yaml.safe_load(file)

    # 准备HTML模板字符串
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Wriggle's Lantern</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 0; }
            .header { text-align: center; margin: 20px 0; }
            table { width: 80%; margin: auto; border-collapse: collapse; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #0ABAB5; color: white; cursor: pointer; }
            th:hover { background-color: #457f43; }
            tr:nth-child(even) { background-color: #f2f2f2; }
            .status200 { background-color: #4CAF50; color: white; }
            .statusError { background-color: #f44336; color: white; }
            img.thumbnail { width: 200px; height: 100px; cursor: pointer; }
            .modal { display: none; position: fixed; z-index: 1; padding-top: 100px; left: 0; top: 0; width: 100%; height: 100%; overflow: auto; background-color: rgb(0,0,0); background-color: rgba(0,0,0,0.9); }
            .modal-content { margin: auto; display: block; width: auto; max-width: none; }
            .close { position: absolute; top: 15px; right: 35px; color: #f1f1f1; font-size: 40px; font-weight: bold; transition: 0.3s; }
            .close:hover, .close:focus { color: #bbb; text-decoration: none; cursor: pointer; }
        </style>
    </head>
    <body>
    
    <div class="header">
        <h1>Now no logo</h1>
    </div>
    
    <table id="resultsTable">
        <thead>
            <tr>
                <th onclick="sortTable(0)">URL</th>
                <th onclick="sortTable(1)">Status Code</th>
                <th onclick="sortTable(2)">Response Time (s)</th>
                <th onclick="sortTable(3)">Title</th>
                <th>Screenshot</th>
            </tr>
        </thead>
        <tbody>
            {% for url, details in data.items() %}
            <tr>
                <td><a href="{{ url }}" target="_blank">{{ url }}</a></td>
                <td class="{{ 'status200' if details.status_code == 200 else 'statusError' if details.status_code != '连接失败' else '' }}">{{ details.status_code }}</td>
                <td>{{ details.response_time }}</td>
                <td>{{ details.title }}</td>
                <td><img src="{{ details.screenshot_path }}" alt="Screenshot" class="thumbnail" onclick="openModal('{{ details.screenshot_path }}')"></td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    
    <div id="myModal" class="modal">
        <span class="close" onclick="closeModal()">&times;</span>
        <img class="modal-content" id="img01">
    </div>
    
    <script>
    function openModal(src) {
        var modal = document.getElementById('myModal');
        var modalImg = document.getElementById('img01');
        modal.style.display = "block";
        modalImg.src = src;
    }
    
    function closeModal() {
        document.getElementById('myModal').style.display = "none";
    }
    
    function sortTable(column) {
        var table, rows, switching, i, x, y, shouldSwitch, dir = "asc", switchcount = 0;
        table = document.getElementById("resultsTable");
        switching = true;
        while (switching) {
            switching = false;
            rows = table.rows;
            for (i = 1; i < (rows.length - 1); i++) {
                shouldSwitch = false;
                x = rows[i].getElementsByTagName("TD")[column];
                y = rows[i + 1].getElementsByTagName("TD")[column];
                if (dir == "asc") {
                    if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                        shouldSwitch = true;
                        break;
                    }
                } else if (dir == "desc") {
                    if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                        shouldSwitch = true;
                        break;
                    }
                }
            }
            if (shouldSwitch) {
                rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
                switching = true;
                switchcount++;
            } else {
                if (switchcount == 0 && dir == "asc") {
                    dir = "desc";
                    switching = true;
                }
            }
        }
    }
    </script>
    
    </body>
    </html>
    """

    # 使用Jinja2模板引擎渲染HTML
    env = Environment(loader=FileSystemLoader('.'))
    template = env.from_string(html_template)
    html_content = template.render(data=data)

    # 保存生成的HTML文件
    html_file_path = f'{now_timestamp_md5()}.html'
    with open(html_file_path, 'w') as html_file:
        html_file.write(html_content)

    print(f"HTML report generated: {html_file_path}")
    return html_file_path

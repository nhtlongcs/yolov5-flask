template = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <title>File sharing</title>

    <!-- Custom stlylesheet -->
    <link href="http://maxcdn.bootstrapcdn.com/font-awesome/4.1.0/css/font-awesome.min.css" rel="stylesheet">
    <link type="text/css" rel="stylesheet" href="css/files.css" />
</head>

<body>

    <div class="ui upload-drop">

        <aside class="ui__sidebar">

            <ul class="file-tree">
                <li class="file-tree__item file-tree__item--open">
                    <div class="folder folder--open"> Images </div>

                    <ul class="file-tree__subtree">
                        <li class="file-tree__item">
                            <div class="folder"> Result </div>
                        </li>
                    </ul>
                    <!-- /.file-subtree -->
            </ul>
            <!-- /.file-tree -->

        </aside>
        <!-- /.sidebar -->

        <main class="ui__main">

            <div class="ui__menu">

                <a href="javascript:void(0);" class="ui__btn sidebar-toggle"></a>
                <a href="javascript:void(0);" data-modal="upload-modal" class="ui__btn upload-btn"></a>
                <ul class="file-path">
                    <li><a href="#"> Images </a></li>
                    <li><a href="#"> Result </a></li>
                </ul>
                <!-- /.file-path -->

                <a href="javascript:void(0);" class="ui__btn options-toggle"></a>
                <a href="javascript:void(0);" class="ui__btn help-btn" data-overlay="help"></a>

            </div>
            <!-- /.ui__menu -->

            <!-- /.ui__info -->

            <table class="file-list" id="file-table">

                <tr class="file-list__header">
                    <th onClick="sortTable(0)">Name <i class="fa fa-long-arrow-down"></i></th>
                    <th onClick="sortTable(1)">Typ</th>
                    <th onClick="sortTable(2, '123')">Size</th>
                    <th>Tags</th>
                </tr>

                {}
            </table>
            <!-- /.file-list -->

        </main>
        <!-- /.ui__main -->

    </div>
    <!-- /.ui -->

    <div class="ui__overlay overlay" id="help">
        <div class="overlay__inner">

            <h2>🎂</h2>
            <p>Only static version</p>

            <a href="javascript:void(0)" class="btn overlay__close">Oh no!</a>

        </div>
        <!-- /.overlay__inner -->
    </div>
    <!-- /.overlay -->

    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
    <script src="./js/files.js"></script>
</body>

</html>
<!-- https://codepen.io/l4ci/pen/PQwdMM -->
"""
block = """
<tr class="file-list__file">
    <td> <a href="{}"> {} </a> </td>
    <td>{}</td>
    <td>{}</td>
    <td>public</td>
</tr>
"""
from glob import glob
import os


def generate(outPath="files.html"):

    root = "shared/"
    items = glob("static/shared/*.jpg")

    def get_ext(inp: str):
        ext = inp.split(".")[-1]
        name = inp.split("/")[-1]
        filesize = "0GB"
        return os.path.join(root, name), name, ext, filesize

    insert_blocks = "\n".join([block.format(*get_ext(x)) for x in items])
    content = template.format(insert_blocks)
    with open(outPath, "w") as f:
        f.write(content)
        f.close()


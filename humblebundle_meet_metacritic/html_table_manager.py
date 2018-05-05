"""
Helper functions to generate table HTML markup
"""

__author__ = "Dean Oemcke"

TD_SEPARATOR = "</td><td>"
TH_SEPARATOR = "</th><th>"


def clean(x):
    try:
        return str(x)
    except:
        return str(x).encode('utf-8')


def generate_table_header(header_list):
    html = '''
    <html>
        <head>
            <style media="screen" type="text/css">
                table {{
                    font-family: sans-serif;
                    font-size: 13px;
                    border-spacing: 0px;
                    border-collapse: collapse;
                }}
        
                tr {{
                    max-height: 15px
                }}
        
                td, th {{
                    border: 1px solid #ccc;
                }}
            </style>
        </head>
        <body>
        <table cellpadding="8" cellspacing="0">
            <thead>
            <tr>
                {theads}
            </tr>
            </thead>
            <tbody>
    '''.format(theads=''.join('<th>{}</th>'.format(str(i)) for i in header_list))
    return html


def generate_table_row(row):
    try:
        html = "<tr>{}</tr>".format(''.join('<td>{}</td>'.format(clean(i)) for i in row))
    except:
        html = '<tr></tr>'
    return html


def generate_table_footer():
    html = '''
            </tbody>
        </table>
    </body>    
    </html>
    '''
    return html


def generate_table_row_sumamry(summary):
    try:
        html = "<tr>{}</tr>".format(clean(summary))
    except:
        html = '<tr></tr>'
    return html

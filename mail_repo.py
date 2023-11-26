'''
    Repository using html and txt templates to create e-mails 
'''


def add_list_items(body, text, file_list):
    for item in file_list:
        body += "<p>%s<p>" % str(item)
        text += str(item) + "\n"
    body += "</body>\n</html>"
    return body, text


def create_report_mail(title, no_of_files, file_list):
    body, text = _get_from_template('report')
    body = body.format(title=title, number_of_files=no_of_files)
    text = text.format(title=title, number_of_files=no_of_files)
    return add_list_items(body, text, file_list)


def _get_from_template(template_name):
    with open('templates/' + template_name + '.html', 'r') as html_file:
        body = html_file.read().replace("\n", "")

    with open('templates/' + template_name + '.txt', 'r') as text_file:
        text = text_file.read()
    return body, text


def _example():
    print(create_report_mail("Triton -> Mediafire", 3))
    print(create_report_mail("", 5))


if __name__ == "__main__":
    _example()


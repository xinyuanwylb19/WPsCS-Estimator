# Impage (logo) Process

import base64

def pic2py(picture_names, py_name):
    write_data = []
    for picture_name in picture_names:
        filename = picture_name.replace('.', '_')
        with open("%s" % picture_name, 'rb') as r:
            b64str = base64.b64encode(r.read())

        write_data.append('%s = "%s"\n' % (filename, b64str.decode()))

    with open(f'{py_name}.py', 'w+') as f:
        for data in write_data:
            f.write(data)

pics = ["logo.jpg"]

pic2py(pics, 'image')
print("Finish...")

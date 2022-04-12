"""Install the modules if you don't have them on your computer,
pip install pillow, pip install qrcode, or simply pip install qrcode[pil]"""

# Library needed
import os, time
import numpy as np
import pandas as pd
from pylab import rcParams
import qrcode
import matplotlib.pyplot as plt
import openpyxl
from openpyxl.drawing.image import Image

# figure size
rcParams['figure.figsize'] = 11, 5


# Function definitions
def Readpref():
    pref = open('pref.txt', 'r')

    pref.close()


def make_excel(dataframe, path, stock_QR, activate=0):
    if activate == 1:

        # write the dataframe into Excel workbook
        dataframe = dataframe.T
        dataframe = dataframe.loc[dataframe.index.repeat(dataframe['N'])]
        dataframe.to_excel(path, index=False, header=True)

        # Add QR images to the Excel workbook for inventory purposes
        book = openpyxl.load_workbook(path)
        ws = book.worksheets[0]

        # Slide number
        nbslide = range(1, len(stock_QR) + 1)
        for n_cell in nbslide:
            ws.cell(row=n_cell + 1, column=12).value = n_cell

        # qrcodes positioning and sheet formatting
        for i, image in enumerate(stock_QR):
            image = image.resize((150, 150))
            image.save("img" + str(i) + ".png", "PNG", quality=200)  # Save your image before inserting
            ws.add_image(Image("img" + str(i) + ".png"), 'U' + str(i + 2))

        # set the height of the row
        for row in range(2, len(stock_QR) + 2, 1):
            ws.row_dimensions[row].height = 120

        # set the width of the column
        ws.column_dimensions['T'].width = 23
        colsheet = ['C', 'U']
        for column in colsheet:
            ws.column_dimensions[column].width = 20

        book.save(path)

        # remove pictures
        for file in os.listdir():
            if file.endswith('.png'):
                os.remove(file)
            else:
                pass

    else:
        pass


def InputCheckpoint(Experimenter, Date, Experiment, Thickness, Target_1, Target_2,
                    Animal, Model, Target_3, Target_4, Cell_ID, N, Birthday, Slice_type, Mounting_medium, Target_5,
                    Target_6, Comment, Animal_ID):
    # Get variables
    saved_args = locals()
    todaydate = time.strftime("%d.%m.%y")

    # My values
    default_values = {'Experimenter': 'Yacine Brahimi', 'Date': todaydate, 'Experiment': 'Immunohistochemistry',
                      'Thickness': '50', 'Target 1': '', 'Target 2': '', 'Animal': "C57BL/6jCrl",
                      'Model': 'Wild Type', 'Target 3': '', 'Target 4': '', 'Cell ID': '', 'N': 1,
                      'Birthday': '', 'Slice type': '', 'Mounting medium': '',
                      'Target 5': '', 'Target 6': '', 'Comment': '', 'Animal_ID': ''}

    # Building default values
    for key, value in saved_args.items():
        if value == '':
            saved_args[key] = default_values.get(key)

    ID = saved_args['Experimenter'][:2] + saved_args['Experiment'][:2] + str(saved_args['Date'].replace('.', '')) \
         + saved_args['Animal'][:3] + \
         ''.join([c for c in saved_args['Model'] if c.isupper()]) + saved_args['Thickness']

    saved_args['Internal ID'] = ID
    saved_args['Thickness'] = saved_args['Thickness'] + ' \u03BCm'

    return saved_args


def generateQR(saved_args, time_str, version, color, path, excel_activate, sequencememory, individual_mode):
    # QR data in Panda dataframe for inventory purposes
    df = pd.DataFrame(saved_args.values(), saved_args.keys())
    df.columns = ['Details']

    # Create the directory where to store our labels
    if not os.path.exists(path):  # If no directory exists
        os.makedirs(path)  # We creat it to store our labels in.
    else:  # Otherwise, if the directory exists,
        pass  # Just move on.

    # Creating an instance of qrcode for each slide
    nQR = int(df.loc['N'].values[0])
    stock_QR = [0] * nQR

    for item in range(nQR):
        df.loc['N'] = item + 1
        input_data = df

        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=0)
        qr.add_data(input_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color=color, back_color='white')
        img = img.resize((500, 500))
        # img.save('Temp/qrcode_' + str(df.loc['N'].values[0]) + '.png',dpi=(1, 1)) # If you just need the QR CODE

        # Create label using matplotlib
        if individual_mode == 1:
            name = str(sequencememory)
        else:
            name = str(df.loc['N'].values[0])
        Label_creation(img, df, name, path, version)

        # Stock Qr images for future use
        stock_QR[item] = img

    make_excel(df, path + '\\' + time_str + '.xlsx', stock_QR, activate=excel_activate)
    return img, df


def Label_creation(img, df, labels, path, version):
    # Make a copy of the dataframe for next loops
    written_data = df.copy()

    # Remove empty optional labels and format data
    InternalID = written_data.loc['Internal ID'].values[0]
    Cell_ID = written_data.loc['Cell_ID'].values[0]

    # concatenate some data, can make a function for this (maybe next update)
    if written_data.loc['Birthday'].values[0] == '':
        pass
    else:
        written_data.loc['Model'] = written_data.loc['Model'] + ' (BD: ' + written_data.loc['Birthday'] + ')'

    if written_data.loc['Animal_ID'].values[0] == '':
        pass
    else:
        written_data.loc['Animal'] = written_data.loc['Animal'] + ' (A. ID: ' + written_data.loc['Animal_ID'] + ')'

    written_data.drop('Comment', axis=0, inplace=True)
    written_data.drop('Birthday', axis=0, inplace=True)
    written_data.drop('Animal_ID', axis=0, inplace=True)
    written_data.drop('N', axis=0, inplace=True)
    written_data.drop('Cell_ID', axis=0, inplace=True)
    written_data.drop('Internal ID', axis=0, inplace=True)
    written_data['Details'].replace('', np.nan, inplace=True)
    written_data.dropna(subset=['Details'], inplace=True)

    # CREATING Labels
    fig, ax = plt.subplots()
    ax.axis('off')
    fig.tight_layout()

    # AXIS 1 - QRCODE for digital records
    ax1 = fig.add_subplot(1, 2, 1)
    ax1.imshow(img, cmap="gray")
    plt.axis('off')
    fig.tight_layout()

    # AXIS 2 - Details for quick viewing
    ax2 = fig.add_subplot(1, 2, 2)
    plt.axis('off')
    fig.tight_layout()

    # write variable inputs
    for i, j in zip(reversed(range(11, 101, 6)), written_data.itertuples()):
        ax2.text(0, i / 100, j[0] + ': ' + str(j[1]), size=17, transform=ax2.transAxes, weight='bold')

    # Write constant inputs
    if Cell_ID:
        ax2.text(0, 0.10, 'Cell ID: ' + Cell_ID, size=17, transform=ax2.transAxes, weight='bold')
    else:
        pass
    ax2.text(0, 0.05, 'Int. ID: ' + InternalID + '_S' + str(labels),
             size=18, transform=ax2.transAxes, weight='bold')
    ax2.text(0, 0, 'SCAN ME to get more details about this slide.  Ya-soft '
             + version, size=10, transform=ax2.transAxes, style='italic')

    # save label and close figure to free up memory for next loops
    fig.savefig(path + '\QR_Slide_' + str(labels) + '.png', dpi=300)  # Change this
    plt.close()

    # reintroduce full dataframe for next loops (important)
    written_data = df

def generate_accept_form_small(doc_data, supplier_data, company_data, product_data, list_data=None,
                               file_path="accept_meat_doc.pdf"):

    from datetime import datetime
    from io import BytesIO
    from django.http import HttpResponse

    from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

    from reportlab.lib import colors
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak

    response = HttpResponse(content_type='application/pdf')
    d = datetime.today().strftime('%Y-%m-%d')
    response['Content-Disposition'] = f'inline; filename="{d}.pdf"'

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, rightMargin=2.5 * cm, leftMargin=2.5 * cm,
                            topMargin=2.5 * cm, bottomMargin=1.5 * cm, title=f'Prijemnica {doc_data["doc_number"]}')

    story = []

    # pdfmetrics.registerFont(TTFont('Verdana', 'verdana.ttf'))
    # pdfmetrics.registerFont(TTFont('Verdana Bold', 'verdanab.ttf'))
    pdfmetrics.registerFont(TTFont('Times', 'times.ttf'))
    pdfmetrics.registerFont(TTFont('Times Bold', 'timesbd.ttf'))

    # Styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Center', fontName='Times', alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='Right', fontName='Times', alignment=TA_RIGHT))
    styles.add(ParagraphStyle(name='Left', fontName='Times', alignment=TA_LEFT))
    styles.add(ParagraphStyle(name='Line_Data_Large', fontName='Times', alignment=TA_LEFT, fontSize=11, leading=11))
    styles.add(ParagraphStyle(name='Table_Label', fontName='Times Bold', fontSize=11, leading=12, alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='Table_Number', fontName='Times', fontSize=11, leading=12, alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='Table_Data', fontName='Times', fontSize=11, leading=11, alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='Line_Label', fontName='Times', fontSize=9, leading=6, alignment=TA_LEFT))
    styles.add(ParagraphStyle(name='Line_Label_C', fontName='Times', fontSize=9, leading=6, alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='Line_Label_R', fontName='Times', fontSize=9, leading=6, alignment=TA_RIGHT))
    styles.add(ParagraphStyle(name='Line_Label_Name', fontName='Times', fontSize=12, leading=6, alignment=TA_LEFT))
    styles.add(ParagraphStyle(name='Line_Label_Center', fontName='Times Bold', fontSize=13, leading=14, alignment=TA_CENTER))

    # Doc start
    # story.append(Spacer(0.1 * cm, 1 * cm))

    story.append(Paragraph("ПРИЈЕМНИЦА<br />ЗА ОТКУПЉЕНА ТОВНА ГРЛА", styles['Line_Label_Center']))

    story.append(Spacer(0.1 * cm, 2 * cm))

    year, month, day = doc_data['doc_date'].split('-')
    srb_date = f'{day}.{month}.{year}.'

    data1 = [
        [Paragraph('Број:', styles['Line_Data_Large']), Paragraph(doc_data['doc_number'], styles['Line_Data_Large']), ''],
        [Paragraph('Датум издавања:', styles['Line_Data_Large']), '', Paragraph(srb_date, styles['Line_Data_Large'])],
        [Paragraph('Место издавања:', styles['Line_Data_Large']), '', Paragraph('KUKUJEVCI', styles['Line_Data_Large'])]
    ]

    t1 = Table(data1, colWidths=(1.5 * cm, 2 * cm, 3.5 * cm))  # , rowHeights = [.3*cm, .5*cm, .3*cm, .5*cm])
    t1.setStyle(TableStyle([
        ('SPAN', (1, 0), (2, 0)),
        ('SPAN', (0, 1), (1, 1)),
        ('SPAN', (0, 2), (1, 2)),
        ('LINEBELOW', (1, 0), (2, 0), 0.25, colors.black),
        ('LINEBELOW', (2, 1), (2, 1), 0.25, colors.black),
        ('LINEBELOW', (2, 2), (2, 2), 0.25, colors.black),
    ]))
    t1.hAlign = 'LEFT'

    story.append(t1)

    story.append(Spacer(0.1 * cm, 0.6 * cm))

    story.append(Table([[Paragraph('ИСПОРУЧИЛАЦ (власник грла)', styles['Line_Label_Name'])]]))

    story.append(Spacer(0.1 * cm, 0.4 * cm))

    data1 = [
        [Paragraph('Име и презиме / Назив', styles['Line_Label'])],
        [Paragraph(supplier_data['supplier_name'], styles['Line_Data_Large'])],
        [Paragraph('JBMG / Матични број', styles['Line_Label'])],
        [Paragraph(supplier_data['id_supplier'], styles['Line_Data_Large'])],
        [Paragraph('Адреса', styles['Line_Label'])],
        [Paragraph(supplier_data['address'], styles['Line_Data_Large'])]
    ]

    t1 = Table(data1, colWidths=(None), rowHeights=[None, 0.8 * cm, None, 0.8 * cm, None, 0.8 * cm])
    # , rowHeights = [.3*cm, .5*cm, .3*cm, .5*cm])
    t1.setStyle(TableStyle([
        ('LINEBELOW', (0, 1), (0, 1), 0.25, colors.black),
        ('LINEBELOW', (0, 3), (0, 3), 0.25, colors.black),
        ('LINEBELOW', (0, 5), (0, 5), 0.25, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    story.append(t1)

    story.append(Spacer(0.1 * cm, 0.6 * cm))

    story.append(Table([[Paragraph('ПРИМАЛАЦ', styles['Line_Label_Name'])]]))

    story.append(Spacer(0.1 * cm, 0.4 * cm))

    data1 = [
        [Paragraph('Назив', styles['Line_Label'])],
        [Paragraph(company_data['company_name'], styles['Line_Data_Large'])],
        [Paragraph('Матични број', styles['Line_Label'])],
        [Paragraph(company_data['id_company'], styles['Line_Data_Large'])],
        [Paragraph('Адреса', styles['Line_Label'])],
        [Paragraph(company_data['address'], styles['Line_Data_Large'])]
    ]

    t1 = Table(data1, colWidths=(None))  # , rowHeights = [.3*cm, .5*cm, .3*cm, .5*cm])
    t1.setStyle(TableStyle([
        ('LINEBELOW', (0, 1), (0, 1), 0.25, colors.black),
        ('LINEBELOW', (0, 3), (0, 3), 0.25, colors.black),
        ('LINEBELOW', (0, 5), (0, 5), 0.25, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    story.append(t1)

    story.append(Spacer(0.1 * cm, 0.6 * cm))

    # Main table
    data1 = [
        [Paragraph('Врста животиња', styles['Table_Label']),
         Paragraph('Број грла', styles['Table_Label']),
         Paragraph('Укупна телесна маса грла', styles['Table_Label']),
         Paragraph('Просечна телесна маса грла', styles['Table_Label']),
         ],
        [Paragraph('1', styles['Table_Number']),
         Paragraph('2', styles['Table_Number']),
         Paragraph('3', styles['Table_Number']),
         Paragraph('4', styles['Table_Number']),
         ],
        [Paragraph(product_data['product_name'], styles['Table_Data']),
         Paragraph(product_data['quantity'], styles['Table_Data']),
         Paragraph(product_data['total_mass'], styles['Table_Data']),
         Paragraph(product_data['mass'], styles['Table_Data']),
         ]
    ]

    t1 = Table(data1, colWidths=(None))  # , rowHeights = [.3*cm, .5*cm, .3*cm, .5*cm])
    t1.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BACKGROUND', (0, 0), (-1, -2), colors.lightgrey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
    ]))

    story.append(t1)

    story.append(Spacer(0.1 * cm, 1 * cm))

    data1 = [
        [Paragraph('Потпис испоручилоца робе', styles['Line_Label_C']),
         '',
         Paragraph('Потпис примаоца робе', styles['Line_Label_C'])
         ],
        ['',
         '',
         ''
         ],
        ['',
         '',
         ''
         ],
        ['',
         '',
         ''
         ]
    ]

    t1 = Table(data1, colWidths=(None, 5 * cm, None))
    t1.setStyle(TableStyle([
        ('BOX', (0, 0), (3, 3), 0.25, colors.black),
        ('LINEBELOW', (0, 2), (0, 2), 0.25, colors.grey),
        ('LINEBELOW', (2, 2), (2, 2), 0.25, colors.grey)
    ]))

    story.append(t1)

    if list_data:
        story.append(PageBreak())

        first_page_pass_limit = 64
        second_page_pass_limit = 160
        sign_size = 13

        address = supplier_data['address']
        if ',' in address:
            pos = address.rfind(',')
            address = address[pos + 1:]
            address = address.strip()

        if len(supplier_data['supplier_name']) < 1:
            supplier_text = ''
            for i in range(51):
                supplier_text += '&nbsp'
        else:
            supplier_text = supplier_data['supplier_name']

        list_text = f"СПИСАК ИД БРОЈЕВА ГРЛА ПРЕДАТИХ КЛАНИЦИ AGROPAPUK DOO,<br/>ДАН {srb_date} ОД {supplier_text} ИЗ {address}"

        story.append(Paragraph(list_text, styles['Line_Data_Large']))

        story.append(Spacer(0.1 * cm, 0.6 * cm))

        empty_line = [
            Paragraph('', styles['Table_Data']),
            Paragraph('', styles['Table_Data']),
            Paragraph('', styles['Table_Data']),
            Paragraph('', styles['Table_Data']),
            Paragraph('', styles['Table_Data'])
        ]

        # quantity = int(product_data['quantity'])

        # Main table
        """
        data1 = [
            [Paragraph('RS', styles['Line_Data_Large']),
             Paragraph('', styles['Line_Data_Large']),
             Paragraph('', styles['Line_Data_Large']),
             Paragraph('', styles['Line_Data_Large']),
             Paragraph('', styles['Line_Data_Large'])
             ]
        ]
        """
        data1 = []

        second_col = 0
        to_fill_empty = False

        passports = tuple(list_data['passports'].splitlines())
        passports_count = len(passports)

        if passports_count <= (first_page_pass_limit // 2):
            rows = passports_count
            to_fill_empty = True
            empty_rows = (first_page_pass_limit // 2) - passports_count
        else:
            rows = (passports_count // 2) + (passports_count % 2)
            second_col = (passports_count // 2)

        tot_f_col_country_count = 0

        for i in range(rows):
            if len(passports[i]) < 4:
                tot_f_col_country_count += 1

        f_col_country_count = 0
        s_col_country_count = 0

        for i in range(rows):
            row = []

            if len(passports[i]) < 4:
                row = [
                    Paragraph(passports[i], styles['Line_Data_Large']),
                    Paragraph('', styles['Table_Data'])
                ]
                f_col_country_count += 1
            else:
                row = [
                    Paragraph(str(i + 1 - f_col_country_count), styles['Table_Data']),
                    Paragraph(passports[i], styles['Table_Data'])
                ]

            row.append(Paragraph('', styles['Table_Data']))

            if second_col != 0 and second_col > i:
                if len(passports[i + rows]) < 4:
                    row.append(Paragraph(passports[i + rows], styles['Line_Data_Large']))
                    row.append(Paragraph('', styles['Table_Data']))
                    s_col_country_count += 1
                else:
                    row.append(Paragraph(str(i + 1 + rows - tot_f_col_country_count - s_col_country_count), styles['Table_Data']))
                    row.append(Paragraph(passports[i + rows], styles['Table_Data']))
            else:
                row.append(Paragraph('', styles['Table_Data']))
                row.append(Paragraph('', styles['Table_Data']))

            data1.append(row)

        if to_fill_empty:
            for _ in range(empty_rows):
                data1.append(empty_line)

        t1 = Table(data1, colWidths=(1.5 * cm, 3.5 * cm, 4.5 * cm, 1.5 * cm, 3.5 * cm), minRowHeights=((.5 * cm,)*(rows+1)))  # , rowHeights = [.3*cm, .5*cm, .3*cm, .5*cm])
        t1.setStyle(TableStyle([
            # ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]))

        story.append(t1)

        if (first_page_pass_limit < passports_count < (first_page_pass_limit + sign_size)
                or second_page_pass_limit < passports_count < (second_page_pass_limit + sign_size)):
            story.append(PageBreak())
        else:
            story.append(Spacer(0.1 * cm, 0.6 * cm))

        list_text = f"ВЕЗА СА УВЕРЕЊЕМ БРОЈ: {list_data['certificate_id']}"

        story.append(Paragraph(list_text, styles['Line_Data_Large']))

        story.append(Spacer(0.1 * cm, .5 * cm))

        list_text = f"No: {list_data['certificate_number']}"

        story.append(Paragraph(list_text, styles['Line_Data_Large']))

        story.append(Spacer(0.1 * cm, 2 * cm))

        data1 = [
            [Paragraph('(ПОТПИС ПРИМАОЦА РОБЕ)', styles['Line_Label_C']),
             '',
             Paragraph('(ПОТПИС ВЕТЕР.ИНСПЕКТ.)', styles['Line_Label_C'])
             ]
        ]

        t1 = Table(data1, colWidths=(None, 3 * cm, None))  # , rowHeights = [.3*cm, .5*cm, .3*cm, .5*cm])
        t1.setStyle(TableStyle([
            ('LINEABOVE', (0, 0), (0, 0), 0.25, colors.black),
            ('LINEABOVE', (-1, 0), (-1, 0), 0.25, colors.black),
        ]))

        story.append(t1)

    doc.build(story)

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response

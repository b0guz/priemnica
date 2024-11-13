import numpy as np
import pandas as pd
from django.contrib.auth.models import User

from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.db import IntegrityError

from otpremnica.models import DispatchNote, Supplier, MeatType, Company


def value_or_null(value):
    if type(value) != int:
        value = value.replace(" ", "")
        if len(value) < 1:
            value = None
    return value


def remove_quotes(value):
    if value is None:
        value = None
    else:
        value = value.replace('"', '')
    return value


def restore_newline(value):
    if value is None:
        value = None
    else:
        value = value.replace('\\n', '\n')
    return value


def import_supplier(request):
    file_name = 'data_s.csv'
    df = pd.read_csv(file_name, dtype=str, delimiter=';')
    df = df.replace(np.nan, None)
    found = 0
    created = 0
    for i in range(1, df.shape[0]):
        supp_id = df.iloc[i, 1]
        try:
            Supplier.objects.get(id_supplier=supp_id)
            found += 1
        except ObjectDoesNotExist:
            name = remove_quotes(df.iloc[i, 0])
            address = remove_quotes(df.iloc[i, 2])
            Supplier.objects.create(id_supplier=supp_id, name=name, address=address)
            created += 1

    context = {'found': found, 'created': created}
    return context


def import_notes(request):
    file_name = 'data_n.csv'
    df = pd.read_csv(file_name, dtype=str, delimiter=';')
    df = df.replace(np.nan, None)
    found = 0
    created = 0
    test = 'index;doc_number;doc_date;total_mass;mass;quantity;passports;cert_id;cert_num;meat_type;supplier;created_by;updated_by'
    for i in range(1, df.shape[0]):
        doc_number = df.iloc[i, 1]
        try:
            DispatchNote.objects.get(doc_number=doc_number)
            found += 1
        except ObjectDoesNotExist:
            index = df.iloc[i, 0]
            doc_date = df.iloc[i, 2]
            total_mass = df.iloc[i, 3]
            mass = df.iloc[i, 4]
            quantity = df.iloc[i, 5]
            passports = restore_newline(df.iloc[i, 6])
            # print(f'passports = {passports}')
            cert_id = restore_newline(df.iloc[i, 7])
            cert_num = restore_newline(df.iloc[i, 8])
            meat_type = MeatType.objects.get(name=df.iloc[i, 9])
            company = Company.objects.first()
            supplier = Supplier.objects.get(id_supplier=df.iloc[i, 10])
            created_by = User.objects.get(username=df.iloc[i, 11])
            upd_user = df.iloc[i, 12]
            if upd_user is not None:
                updated_by = User.objects.get(username=upd_user)
            else:
                updated_by = None

            DispatchNote.objects.create(
                index=index,
                doc_number=doc_number,
                doc_date=doc_date,
                supplier=supplier,
                company=company,
                meat_type=meat_type,
                quantity=quantity,
                total_mass=total_mass,
                mass=mass,
                passports=passports,
                certificate_id=cert_id,
                certificate_number=cert_num,
                created_by=created_by,
                updated_by=updated_by
            )

            created += 1

    context = {'found': found, 'created': created}
    return context


def import_docs(request):
    file2 = 'todo.xlsx'

    xlsx = pd.ExcelFile(file2)
    df = pd.read_excel(xlsx, index_col=None, dtype=object)

    df = df.fillna("")

    x = df.shape[1]
    y = df.shape[0]

    count = 0

    last_note = DispatchNote.objects.last()
    if last_note is None:
        db_index = 0
    else:
        db_index = getattr(last_note, 'index')

    message = ''

    for index, row in df.iterrows():
        number = df.iloc[index, 0]
        date = df.iloc[index, 1]
        name = df.iloc[index, 2]
        jbmg = df.iloc[index, 3]
        address = df.iloc[index, 4]
        meat_type = df.iloc[index, 5]
        quantity = df.iloc[index, 6]
        total_mass = df.iloc[index, 7]
        mass = df.iloc[index, 8]
        passports = df.iloc[index, 9]
        certificate_id = df.iloc[index, 10]
        certificate_number = df.iloc[index, 11]

        if '.' in date:
            date = date.replace(".", "-")
            if date[-1] == '-':
                date = date[:-1]
            new_date = datetime.strptime(date, "%d-%m-%Y").date()
        else:
            new_date = date

        if type(jbmg) != float:
            jbmg = jbmg.replace(" ", "")

        quantity = value_or_null(quantity)
        total_mass = value_or_null(total_mass)
        mass = value_or_null(mass)

        print(f'\nnumber = {number}')

        print(f'quantity={quantity}, type={type(quantity)}')
        print(f'total_mass={total_mass}, type={type(total_mass)}')
        print(f'mass={mass}, type={type(mass)}')

        # quantity = quantity.replace(" ", "")
        # total_mass = total_mass.replace(" ", "")
        # mass = mass.replace(" ", "")

        # total_mass = convert_decimal(df.iloc[index, 7])
        # mass = convert_decimal(df.iloc[index, 8])

        """
        print(f'date = {date}')
        print(f'new_date = {new_date}')
        # print(f'date-1 = {date[-1]}')
        print(f'type(date) = {type(date)}')
        """
        # print(f'tm_type = {type(total_mass)}')

        print(f'jbmg = {jbmg}')
        print(f'len jbmg = {len(jbmg)}')
        print(f'jbmg_type = {type(jbmg)}')

        if len(jbmg) < 1:
            supplier = Supplier.objects.get(id_supplier='00000')
        else:
            try:
                supplier = Supplier.objects.get(id_supplier=jbmg)
            except ObjectDoesNotExist:
                supplier = Supplier.objects.create(name=name,
                                                   id_supplier=jbmg,
                                                   address=address)

        meat_selection = MeatType.objects.get(name=meat_type)

        company = Company.objects.last()

        print(f'supplier = {supplier}')
        print(f'meat_selection = {meat_selection}')

        """
        print('---')
        print(f'passports = {passports}')
        print(f'type passports = {type(passports)}')
        print(f'len passports = {len(passports)}')
        """

        if len(passports) < 4:
            passports = None
            certificate_id = None
            certificate_number = None
        else:
            passports = passports.replace("[", "")
            passports = passports.replace("]", "")
            passports = passports.replace("'", "")
            passports = passports.replace(" ", "")
            passports = passports.replace(",", "\n")

        print(f'index = {index}')

        try:
            DispatchNote.objects.create(
                index=int(index) + 1 + db_index,
                doc_number=number,
                doc_date=new_date,
                supplier=supplier,
                company=company,
                meat_type=meat_selection,
                quantity=quantity,
                total_mass=total_mass,
                mass=mass,
                passports=passports,
                certificate_id=certificate_id,
                certificate_number=certificate_number,
                created_by=request.user
            )
        except IntegrityError:
            message = f'Not unique doc_number {number}'

        count += 1

    xlsx.close()

    context = {'data_x': x, 'data_y': y, 'count': count, 'message': message}
    return context

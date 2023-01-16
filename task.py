import pdfplumber
import pandas as pd
import glob
import os


# defining the function used in main()
def get_keyword(start, end, text):
    """
    start: the word prior to the keyword
    end: the word that comes after the keyword
    text: the text from the page(s) just extracted
    """
    for i in range(len(start)):
        try:
            field = ((text.split(start[i]))[1].split(end[i])[0])
            return field
        except:
            continue


def main():
    # create an empty dataframe, from which keywords from multiple .pdf files will be later append by rows
    my_dataframe = pd.DataFrame()
    for files in glob.glob(r"C:\Users\E1328977\Desktop\Robocorp-trainingprojects\Robocorp-trainingprojects\MSOL_682_Supplier_Price_validity_log_for_Manifolds\MSOL_682_robo_py\PDF\*.pdf"):
        with pdfplumber.open(files) as pdf:
            page = pdf.pages[0]
            text = page.extract_text()
            text = " ".join(text.split())
            # print(text)

            # obtain key : Supplier
            Supplier = 'SCHNEIDER'

            # obtain key : PartNumber
            start = [' RON 10 ']
            end = [' ']
            PartNumber = get_keyword(start, end, text)
            if PartNumber is None:
                start = [' EUR 10 ']
                end = [' ']
                PartNumber = get_keyword(start, end, text)
            if PartNumber == '000000':  # TODO find something to extract only the Part
                start = ['PC 1 ']
                end = ['..T']
                PartNumber = str(get_keyword(start, end, text))[14:40]
            if PartNumber is None:
                with pdfplumber.open(files) as pdf:
                    page = pdf.pages[1]
                    text = page.extract_text()
                    text = " ".join(text.split())
                    start = [' RON 10 ']
                    end = [' ']
                    PartNumber = get_keyword(start, end, text)
                    if PartNumber is None:
                        start = [' EUR 10 ']
                        end = [' ']
                        PartNumber = get_keyword(start, end, text)
                    if PartNumber == '000000':  # TODO find something to extract only the Part
                        start = ['PC 1 ']
                        end = ['..T']
                        PartNumber = str(get_keyword(start, end, text))[14:40]

        # obtain key : Number of pieces Quantity10
            start = [' RON 10 ']
            end = [' PC ']
            var13 = str(get_keyword(start, end, text))
            start1 = [' ']
            end1 = [' ']
            Quantity = get_keyword(start1, end1, var13)
            if Quantity is None:
                start = [' EUR 10 ']
                end = [' PC ']
                var13 = str(get_keyword(start, end, text))
                start1 = [' ']
                end1 = [' ']
                Quantity = get_keyword(start1, end1, var13)

        # obtain key : Supplier Quote
            start = ['Quotation No. : ']
            end = [' ']
            SupplierQuote = get_keyword(start, end, text)
            # print(SupplierQuote)

        # obtain key : CostFromSupplier
            start = ['PC 1 ']
            end = [' ']
            CostFromSupplier = get_keyword(start, end, text)
            if len(str(CostFromSupplier)) < 3:
                try:
                    start = ['PC 1 ']
                    end = ['A']
                    CostFromSupplier = str(get_keyword(start, end, text))[:9]
                except TypeError:
                    CostFromSupplier = "You don't have more items"

        # obtain key : Currency
            start = ['Description ']
            end = [' ']
            Currency = get_keyword(start, end, text)

        # obtain key : LeadTime
            start = ['Del. within : ']
            end = [' 11']
            LeadTime = get_keyword(start, end, text)
            if LeadTime == None:
                with pdfplumber.open(files) as pdf:
                    page = pdf.pages[1]
                    text = page.extract_text()
                    text = " ".join(text.split())
                    start = ['Del. within : ']
                    end = [' 11']
                    LeadTime = get_keyword(start, end, text)
        # obtain key : PriceValidity
            start = ['This quotation is valid until ']
            end = [' ']
            PriceValidity = get_keyword(start, end, text)
            if PriceValidity == None:
                with pdfplumber.open(files) as pdf:
                    page = pdf.pages[1]
                    text = page.extract_text()
                    text = " ".join(text.split())
                    start = ['This quotation is valid until ']
                    end = [' ']
                    PriceValidity = get_keyword(start, end, text)
                    if PriceValidity == None:
                        with pdfplumber.open(files) as pdf:
                            page = pdf.pages[2]
                            text = page.extract_text()
                            text = " ".join(text.split())
                            start = ['This quotation is valid until ']
                            end = [' ']
                            PriceValidity = get_keyword(start, end, text)
                            if PriceValidity == None:
                                with pdfplumber.open(files) as pdf:
                                    page = pdf.pages[3]
                                    text = page.extract_text()
                                    text = " ".join(text.split())
                                    start = ['This quotation is valid until ']
                                    end = [' ']
                                    PriceValidity = get_keyword(
                                        start, end, text)
                                    if PriceValidity == None:
                                        with pdfplumber.open(files) as pdf:
                                            page = pdf.pages[4]
                                            text = page.extract_text()
                                            text = " ".join(text.split())
                                            start = [
                                                'This quotation is valid until ']
                                            end = [' ']
                                            PriceValidity = get_keyword(
                                                start, end, text)
                                            if PriceValidity == None:
                                                with pdfplumber.open(files) as pdf:
                                                    page = pdf.pages[5]
                                                    text = page.extract_text()
                                                    text = " ".join(
                                                        text.split())
                                                    start = [
                                                        'This quotation is valid until ']
                                                    end = [' ']
                                                    PriceValidity = get_keyword(
                                                        start, end, text)
                                                    if PriceValidity == None:
                                                        with pdfplumber.open(files) as pdf:
                                                            page = pdf.pages[6]
                                                            text = page.extract_text()
                                                            text = " ".join(
                                                                text.split())
                                                            start = [
                                                                'This quotation is valid until ']
                                                            end = [' ']
                                                            PriceValidity = get_keyword(
                                                                start, end, text)
                                                            if PriceValidity == None:
                                                                with pdfplumber.open(files) as pdf:
                                                                    page = pdf.pages[7]
                                                                    text = page.extract_text()
                                                                    text = " ".join(
                                                                        text.split())
                                                                    start = [
                                                                        'This quotation is valid until ']
                                                                    end = [' ']
                                                                    PriceValidity = get_keyword(
                                                                        start, end, text)
        # obtain key : PartNumber20
            start = [' 20 ']
            end = [' ']
            PartNumber20 = get_keyword(start, end, text)
            if PartNumber20 is None:
                with pdfplumber.open(files) as pdf:
                    page = pdf.pages[1]
                    text = page.extract_text()
                    text = " ".join(text.split())
                    start = [' 20 ']
                    end = [' ']
                    PartNumber20 = get_keyword(start, end, text)
                    if PartNumber20 == '000000':
                        start = [' 20 ']
                        end = ['..T']
                        PartNumber20 = str(
                            get_keyword(start, end, text))[25:50]
                    # if PartNumber20 is on 3th page
                    if PartNumber20 is None:
                        try:
                            with pdfplumber.open(files) as pdf:
                                page = pdf.pages[2]
                                text = page.extract_text()
                                text = " ".join(text.split())
                                start = [' 20 ']
                                end = [' ']
                                PartNumber20 = get_keyword(start, end, text)
                                if PartNumber20 == '000000':
                                    start = [' 20 ']
                                    end = ['..T']
                                    PartNumber20 = str(
                                        get_keyword(start, end, text))[25:50]
                        except IndexError:
                            PartNumber20 = get_keyword(start, end, text)

        # obtain key : Number of pieces Quantity20
            start = [' 20 ']
            end = [' PC ']
            var14 = str(get_keyword(start, end, text))
            start1 = [' ']
            end1 = [' ']
            Quantity20 = get_keyword(start1, end1, var14)

        # obtain key for : LeadTime20
            # I extracted the text related to item 20 and stored it in a variable
            start = [' 20 ']
            end = [' 21 ']
            var1 = str(get_keyword(start, end, text))
            global LeadTime20
            # From the text of item 20, we extract the lead-time, the specific text between 'Del.within' and 21
            if var1 is not None:
                start = [' Del. within : ']
                end = [' 21 ']
                LeadTime20 = str(get_keyword(start, end, var1))
                # If the text does not end with 21, but with 'Q', we take Q as a reference
                if len(LeadTime20) > 11:
                    start = [' Del. within : ']
                    end = [' Q']
                    LeadTime20 = str(get_keyword(start, end, var1))
                # if the text does not end with 21, but with '30', we take 30 as a reference
                    if len(LeadTime20) > 11:
                        start = [' Del. within : ']
                        end = [' 30 ']
                        LeadTime20 = get_keyword(start, end, var1)
                # If LeadTime 20 is on the other page
                if LeadTime20 == 'None':
                    try:
                        with pdfplumber.open(files) as pdf:
                            page = pdf.pages[2]
                            text = page.extract_text()
                            text = " ".join(text.split())
                            start = [' Del. within : ']
                            end = [' 21 ']
                            LeadTime20 = str(get_keyword(start, end, text))
                            if len(LeadTime20) > 20:
                                start = [' Del. within : ']
                                end = [' 31 ']
                                LeadTime20 = get_keyword(start, end, text)
                    except IndexError:
                        LeadTime20 = str(get_keyword(start, end, var1))

        # obtain key for : CostFromSupplier20
        with pdfplumber.open(files) as pdf:
            page = pdf.pages[1]
            text = page.extract_text()
            text = " ".join(text.split())
            start = [' 20 ']
            end = [' 21 ']
            var2 = str(get_keyword(start, end, text))
            CostFromSupplier20 = " "
            # IF YOU FIND SOMETHING ON PAGE  1
            if var2 != 'None':
                start = [' PC 1 ']
                end = ['A']
                CostFromSupplier20 = str(get_keyword(start, end, var2))[:8]

            # IF YOU FIND SOMETHING ON PAGE  2
            if var2 == 'None':
                try:
                    with pdfplumber.open(files) as pdf:
                        page = pdf.pages[2]
                        text = page.extract_text()
                        text = " ".join(text.split())
                        start = [' 20 ']
                        end = [' 21 ']
                        var2 = str(get_keyword(start, end, text))
                        if var2 != 'None':
                            start = [' PC 1 ']
                            end = ['A']
                            CostFromSupplier20 = str(
                                get_keyword(start, end, var2))[:8]
                except IndexError:
                    CostFromSupplier20 = "You don't have more items"

    # obtain key for : PartNumber30
        with pdfplumber.open(files) as pdf:
            page = pdf.pages[1]
            text = page.extract_text()
            text = " ".join(text.split())
            start = [' 30 ']
            end = [' ']
            PartNumber30 = get_keyword(start, end, text)
            if PartNumber30 == '000000':
                start = [' 30 ']
                end = ['..T']
                PartNumber30 = str(get_keyword(start, end, text))[25:50]
            if PartNumber30 is None:
                try:
                    with pdfplumber.open(files) as pdf:
                        page = pdf.pages[2]
                        text = page.extract_text()
                        text = " ".join(text.split())
                        start = [' 30 ']
                        end = [' ']
                        PartNumber30 = get_keyword(start, end, text)
                        if PartNumber30 == '000000':
                            start = [' 30 ']
                            end = ['..T']
                            PartNumber30 = str(
                                get_keyword(start, end, text))[25:50]

                        if PartNumber30 is None:
                            with pdfplumber.open(files) as pdf:
                                page = pdf.pages[3]
                                text = page.extract_text()
                                text = " ".join(text.split())
                                start = [' 30 ']
                                end = [' ']
                                PartNumber30 = get_keyword(
                                    start, end, text)
                                if PartNumber30 == '000000':
                                    start = [' 30 ']
                                    end = ['..T']
                                    PartNumber30 = str(
                                        get_keyword(start, end, text))[25:50]
                except IndexError:
                    continue

    # obtain key : Number of pieces Quantity30
        # Search quantity30 on page 2
        with pdfplumber.open(files) as pdf:
            page = pdf.pages[1]
            text = page.extract_text()
            text = " ".join(text.split())
            start = [' 30 ']
            end = [' PC ']
            var15 = str(get_keyword(start, end, text))
            start1 = [' ']
            end1 = [' ']
            Quantity30 = get_keyword(start1, end1, var15)
            if Quantity30 is None:
                # Search quantity30 on page 3
                try:
                    with pdfplumber.open(files) as pdf:
                        page = pdf.pages[2]
                        text = page.extract_text()
                        text = " ".join(text.split())
                        start = [' 30 ']
                        end = [' PC ']
                        var15 = str(get_keyword(start, end, text))
                        start1 = [' ']
                        end1 = [' ']
                        Quantity30 = get_keyword(start1, end1, var15)
                except IndexError:
                    Quantity30 = "You don't have more items"
            if Quantity30 is None:
                try:
                    # Search quantity30 on page 4
                    with pdfplumber.open(files) as pdf:
                        page = pdf.pages[3]
                        text = page.extract_text()
                        text = " ".join(text.split())
                        start = [' 30 ']
                        end = [' PC ']
                        var15 = str(get_keyword(start, end, text))
                        start1 = [' ']
                        end1 = [' ']
                        Quantity30 = get_keyword(start1, end1, var15)
                except IndexError:
                    Quantity30 = "You don't have more items"

    # obtain key for : LeadTime30
        with pdfplumber.open(files) as pdf:
            page = pdf.pages[1]
            text = page.extract_text()
            text = " ".join(text.split())
            start = [' 30 ']
            end = [' 31 ']
            var3 = str(get_keyword(start, end, text))
            LeadTime30 = " "
            # IF YOU FIND SOMETHING ON PAGE  2
            if var3 != 'None':
                start = [' Del. within : ']
                end = [' 31 ']
                LeadTime30 = str(get_keyword(start, end, var3))
                # If the text does not end with 31, but with 'Q', we take Q as a reference
                if len(LeadTime30) > 11:
                    start = [' Del. within : ']
                    end = [' Q']
                    LeadTime30 = str(get_keyword(start, end, var3))
                # if the text does not end with 31, but with '30', we take 30 as a reference
                    if len(LeadTime30) > 11:
                        start = [' Del. within : ']
                        end = [' 40 ']
                        LeadTime30 = str(get_keyword(start, end, var3))

                # WE HAVE ON PAGE 2 ITEM30, BUT DEL WITHIN IS ON PAGE 3
                if LeadTime30 == 'None':
                    try:
                        with pdfplumber.open(files) as pdf:
                            page = pdf.pages[2]
                            text = page.extract_text()
                            text = " ".join(text.split())
                            start = [' Del. within : ']
                            end = [' 31 ']
                            LeadTime30 = str(
                                get_keyword(start, end, text))
                    except IndexError:
                        LeadTime30 = "You don't have more items"

            # IF YOU FIND SOMETHING ON PAGE  3
            if var3 == 'None':
                try:
                    with pdfplumber.open(files) as pdf:
                        page = pdf.pages[2]
                        text = page.extract_text()
                        text = " ".join(text.split())
                        start = [' 30 ']
                        end = [' 31 ']
                        var3 = str(get_keyword(start, end, text))
                        if var3 != 'None':
                            start = [' Del. within : ']
                            end = [' 31 ']
                            LeadTime30 = str(get_keyword(start, end, var3))
                            # If the text does not end with 31, but with 'Q', we take Q as a reference
                            if len(LeadTime30) > 11:
                                start = [' Del. within : ']
                                end = [' Q']
                                LeadTime30 = str(get_keyword(start, end, var3))
                            # if the text does not end with 31, but with '30', we take 30 as a reference
                                if len(LeadTime30) > 11:
                                    start = [' Del. within : ']
                                    end = [' 40 ']
                                    LeadTime30 = str(
                                        get_keyword(start, end, var3))
                            # WE HAVE ON PAGE3 ITEM 30, BUT DEL WITHIN IS ON PAGE 4
                            if LeadTime30 == 'None':
                                with pdfplumber.open(files) as pdf:
                                    page = pdf.pages[3]
                                    text = page.extract_text()
                                    text = " ".join(text.split())
                                    start = [' Del. within : ']
                                    end = [' 31 ']
                                    LeadTime30 = str(
                                        get_keyword(start, end, text))
                except IndexError:
                    LeadTime30 = "You don't have more items"
            # IF YOU FIND SOMETHING ON PAGE  4
            if var3 == 'None':
                try:
                    with pdfplumber.open(files) as pdf:
                        page = pdf.pages[3]
                        text = page.extract_text()
                        text = " ".join(text.split())
                        start = [' 30 ']
                        end = [' 31 ']
                        var3 = str(get_keyword(start, end, text))
                        if var3 != 'None':
                            start = [' Del. within : ']
                            end = [' 31 ']
                            LeadTime30 = str(get_keyword(start, end, var3))
                            # If the text does not end with 31, but with 'Q', we take Q as a reference
                            if len(LeadTime30) > 11:
                                start = [' Del. within : ']
                                end = [' Q']
                                LeadTime30 = str(get_keyword(start, end, var3))
                            # if the text does not end with 31, but with '30', we take 30 as a reference
                                if len(LeadTime30) > 11:
                                    start = [' Del. within : ']
                                    end = [' 40 ']
                                    LeadTime30 = str(get_keyword(
                                        start, end, var3))
                            # WE HAVE ON PAGE4 ITEM 30, BUT DEL WITHIN IS ON PAGE 5
                            if LeadTime30 == 'None':
                                with pdfplumber.open(files) as pdf:
                                    page = pdf.pages[4]
                                    text = page.extract_text()
                                    text = " ".join(text.split())
                                    start = [' Del. within : ']
                                    end = [' 31 ']
                                    LeadTime30 = str(
                                        get_keyword(start, end, text))
                except IndexError:
                    LeadTime30 = "You don't have more items"

        # obtain key for : CostFromSupplier30
        with pdfplumber.open(files) as pdf:
            page = pdf.pages[1]
            text = page.extract_text()
            text = " ".join(text.split())
            start = [' 30 ']
            end = [' 31 ']
            var4 = str(get_keyword(start, end, text))
            CostFromSupplier30 = " "
            # IF YOU FIND SOMETHING ON PAGE  2
            if var4 != 'None':
                start = [' PC 1 ']
                end = ['A']
                CostFromSupplier30 = str(get_keyword(start, end, var4))[:8]

            # IF YOU FIND SOMETHING ON PAGE  3
            if var4 == 'None':
                try:
                    with pdfplumber.open(files) as pdf:
                        page = pdf.pages[2]
                        text = page.extract_text()
                        text = " ".join(text.split())
                        start = [' 30 ']
                        end = [' 31 ']
                        var4 = str(get_keyword(start, end, text))
                        if var4 != 'None':
                            start = [' PC 1 ']
                            end = ['A']
                            CostFromSupplier30 = str(
                                get_keyword(start, end, var4))[:8]
                except IndexError:
                    CostFromSupplier30 = "You don't have more items"

            # IF YOU FIND SOMETHING ON PAGE  4
            if var4 == 'None':
                try:
                    with pdfplumber.open(files) as pdf:
                        page = pdf.pages[3]
                        text = page.extract_text()
                        text = " ".join(text.split())
                        start = [' 30 ']
                        end = [' 31 ']
                        var4 = str(get_keyword(start, end, text))
                        if var4 != 'None':
                            start = [' PC 1 ']
                            end = ['A']
                            CostFromSupplier30 = str(
                                get_keyword(start, end, var4))[:8]
                except IndexError:
                    CostFromSupplier30 = "You don't have more items"

        # obtain key for : PartNumber40
        with pdfplumber.open(files) as pdf:
            page = pdf.pages[2]
            text = page.extract_text()
            text = " ".join(text.split())
            start = [' 40 ']
            end = [' ']
            PartNumber40 = get_keyword(start, end, text)
            if PartNumber40 == '000000':
                start = [' 40 ']
                end = ['..T']
                PartNumber40 = str(get_keyword(start, end, text))[25:50]
            if PartNumber40 is None:
                try:
                    with pdfplumber.open(files) as pdf:
                        page = pdf.pages[3]
                        text = page.extract_text()
                        text = " ".join(text.split())
                        start = [' 40 ']
                        end = [' ']
                        PartNumber40 = get_keyword(start, end, text)
                        if PartNumber40 == '000000':
                            start = [' 40 ']
                            end = ['..T']
                            PartNumber40 = str(
                                get_keyword(start, end, text))[25:50]

                        if PartNumber40 is None:
                            with pdfplumber.open(files) as pdf:
                                page = pdf.pages[4]
                                text = page.extract_text()
                                text = " ".join(text.split())
                                start = [' 40 ']
                                end = [' ']
                                PartNumber40 = get_keyword(
                                    start, end, text)
                                if PartNumber40 == '000000':
                                    start = [' 40 ']
                                    end = ['..T']
                                    PartNumber40 = str(
                                        get_keyword(start, end, text))[25:50]
                except IndexError:
                    PartNumber40 = "You don't have more items"

        # obtain key : Number of pieces Quantity40
        # Search quantity40 on page 3
        with pdfplumber.open(files) as pdf:
            try:
                page = pdf.pages[2]
                text = page.extract_text()
                text = " ".join(text.split())
                start = [' 40 ']
                end = [' PC ']
                var16 = str(get_keyword(start, end, text))
                start1 = [' ']
                end1 = [' ']
                Quantity40 = get_keyword(start1, end1, var16)
                if Quantity40 is None:
                    # Search quantity40 on page 4
                    with pdfplumber.open(files) as pdf:
                        page = pdf.pages[3]
                        text = page.extract_text()
                        text = " ".join(text.split())
                        start = [' 40 ']
                        end = [' PC ']
                        var16 = str(get_keyword(start, end, text))
                        start1 = [' ']
                        end1 = [' ']
                        Quantity40 = get_keyword(start1, end1, var16)
                if Quantity40 is None:
                    # Search quantity40 on page 5
                    with pdfplumber.open(files) as pdf:
                        page = pdf.pages[4]
                        text = page.extract_text()
                        text = " ".join(text.split())
                        start = [' 40 ']
                        end = [' PC ']
                        var16 = str(get_keyword(start, end, text))
                        start1 = [' ']
                        end1 = [' ']
                        Quantity40 = get_keyword(start1, end1, var16)
            except IndexError:
                Quantity40 = "You don't have more items"

        # obtain key for : LeadTime40
        with pdfplumber.open(files) as pdf:
            page = pdf.pages[2]
            text = page.extract_text()
            text = " ".join(text.split())
            start = [' 40 ']
            end = [' 41 ']
            var5 = str(get_keyword(start, end, text))
            LeadTime40 = " "
            # IF YOU FIND SOMETHING ON PAGE  3
            if var5 != 'None':
                start = [' Del. within : ']
                end = [' 41 ']
                LeadTime40 = str(get_keyword(start, end, var5))
                # If the text does not end with 41, but with 'Q', we take Q as a reference
                if len(LeadTime40) > 11:
                    start = [' Del. within : ']
                    end = [' Q']
                    LeadTime40 = str(get_keyword(start, end, var5))
                # if the text does not end with 41, but with '30', we take 30 as a reference
                    if len(LeadTime40) > 11:
                        start = [' Del. within : ']
                        end = [' 41 ']
                        LeadTime40 = str(get_keyword(start, end, var5))

                # WE HAVE ON PAGE3 ITEM 40, BUT DEL WITHIN IS ON PAGE 4
                if LeadTime40 == 'None':
                    try:
                        with pdfplumber.open(files) as pdf:
                            page = pdf.pages[3]
                            text = page.extract_text()
                            text = " ".join(text.split())
                            start = [' Del. within : ']
                            end = [' 41 ']
                            LeadTime40 = str(
                                get_keyword(start, end, text))
                    except IndexError:
                        LeadTime40 = "You don't have more items"

            # IF YOU FIND SOMETHING ON PAGE  4
            if var5 == 'None':
                try:
                    with pdfplumber.open(files) as pdf:
                        page = pdf.pages[3]
                        text = page.extract_text()
                        text = " ".join(text.split())
                        start = [' 40 ']
                        end = [' 41 ']
                        var5 = str(get_keyword(start, end, text))
                        if var5 != 'None':
                            start = [' Del. within : ']
                            end = [' 41 ']
                            LeadTime40 = str(get_keyword(start, end, var5))
                            # If the text does not end with 41, but with 'Q', we take Q as a reference
                            if len(LeadTime40) > 11:
                                start = [' Del. within : ']
                                end = [' Q']
                                LeadTime40 = str(get_keyword(start, end, var5))
                            # if the text does not end with 41, but with '30', we take 30 as a reference
                                if len(LeadTime40) > 11:
                                    start = [' Del. within : ']
                                    end = [' 40 ']
                                    LeadTime40 = str(
                                        get_keyword(start, end, var5))
                            # WE HAVE ON PAGE4 ITEM 40, BUT DEL WITHIN IS ON PAGE 5
                            if LeadTime40 == 'None':
                                with pdfplumber.open(files) as pdf:
                                    page = pdf.pages[4]
                                    text = page.extract_text()
                                    text = " ".join(text.split())
                                    start = [' Del. within : ']
                                    end = [' 41 ']
                                    LeadTime40 = str(
                                        get_keyword(start, end, text))
                except IndexError:
                    LeadTime40 = "You don't have more items"
            # IF YOU FIND SOMETHING ON PAGE  5
            if var5 == 'None':
                try:
                    with pdfplumber.open(files) as pdf:
                        page = pdf.pages[4]
                        text = page.extract_text()
                        text = " ".join(text.split())
                        start = [' 40 ']
                        end = [' 41 ']
                        var5 = str(get_keyword(start, end, text))
                        if var5 != 'None':
                            start = [' Del. within : ']
                            end = [' 41 ']
                            LeadTime40 = str(get_keyword(start, end, var5))
                            # If the text does not end with 41, but with 'Q', we take Q as a reference
                            if len(LeadTime40) > 11:
                                start = [' Del. within : ']
                                end = [' Q']
                                LeadTime40 = str(get_keyword(start, end, var5))
                            # if the text does not end with 41, but with '30', we take 30 as a reference
                                if len(LeadTime40) > 11:
                                    start = [' Del. within : ']
                                    end = [' 40 ']
                                    LeadTime40 = str(get_keyword(
                                        start, end, var5))
                            # WE HAVE ON PAGE5 ITEM 40, BUT DEL WITHIN IS ON PAGE 6
                            if LeadTime40 == 'None':
                                with pdfplumber.open(files) as pdf:
                                    page = pdf.pages[5]
                                    text = page.extract_text()
                                    text = " ".join(text.split())
                                    start = [' Del. within : ']
                                    end = [' 41 ']
                                    LeadTime40 = str(
                                        get_keyword(start, end, text))
                except IndexError:
                    LeadTime40 = "You don't have more items"

        # obtain key for : CostFromSupplier40
        with pdfplumber.open(files) as pdf:
            page = pdf.pages[2]
            text = page.extract_text()
            text = " ".join(text.split())
            start = [' 40 ']
            end = [' 41 ']
            var6 = str(get_keyword(start, end, text))
            CostFromSupplier40 = " "
            # IF YOU FIND SOMETHING ON PAGE  3
            if var6 != 'None':
                start = [' PC 1 ']
                end = ['A']
                CostFromSupplier40 = str(get_keyword(start, end, var6))[:8]

            # IF YOU FIND SOMETHING ON PAGE  4
            if var6 == 'None':
                try:
                    with pdfplumber.open(files) as pdf:
                        page = pdf.pages[3]
                        text = page.extract_text()
                        text = " ".join(text.split())
                        start = [' 40 ']
                        end = [' 41 ']
                        var6 = str(get_keyword(start, end, text))
                        if var6 != 'None':
                            start = [' PC 1 ']
                            end = ['A']
                            CostFromSupplier40 = str(
                                get_keyword(start, end, var6))[:8]
                except IndexError:
                    CostFromSupplier40 = "You don't have more items"

            # IF YOU FIND SOMETHING ON PAGE  5
            if var6 == 'None':
                try:
                    with pdfplumber.open(files) as pdf:
                        page = pdf.pages[4]
                        text = page.extract_text()
                        text = " ".join(text.split())
                        start = [' 40 ']
                        end = [' 41 ']
                        var6 = str(get_keyword(start, end, text))
                        if var6 != 'None':
                            start = [' PC 1 ']
                            end = ['A']
                            CostFromSupplier40 = str(
                                get_keyword(start, end, var6))[:8]
                except IndexError:
                    CostFromSupplier40 = "You don't have more items"

        # obtain key for : PartNumber50
        with pdfplumber.open(files) as pdf:
            try:
                page = pdf.pages[3]
                text = page.extract_text()
                text = " ".join(text.split())
                start = [' 50 ']
                end = [' ']
                PartNumber50 = get_keyword(start, end, text)
                if PartNumber50 == '000000':
                    start = [' 50 ']
                    end = ['..T']
                    PartNumber50 = str(get_keyword(start, end, text))[25:50]
                if PartNumber50 is None:
                    with pdfplumber.open(files) as pdf:
                        page = pdf.pages[4]
                        text = page.extract_text()
                        text = " ".join(text.split())
                        start = [' 50 ']
                        end = [' ']
                        PartNumber50 = get_keyword(start, end, text)
                        if PartNumber50 == '000000':
                            start = [' 50 ']
                            end = ['..T']
                            PartNumber50 = str(
                                get_keyword(start, end, text))[25:50]

                        if PartNumber50 is None:
                            with pdfplumber.open(files) as pdf:
                                page = pdf.pages[5]
                                text = page.extract_text()
                                text = " ".join(text.split())
                                start = [' 50 ']
                                end = [' ']
                                PartNumber50 = get_keyword(
                                    start, end, text)
                                if PartNumber50 == '000000':
                                    start = [' 50 ']
                                    end = ['..T']
                                    PartNumber50 = str(
                                        get_keyword(start, end, text))[25:50]
            except IndexError:
                PartNumber50 = "You don't have more items"

        # obtain key : Number of pieces Quantity50
        # Search quantity50 on page 4
        with pdfplumber.open(files) as pdf:
            try:
                page = pdf.pages[3]
                text = page.extract_text()
                text = " ".join(text.split())
                start = [' 50 ']
                end = [' PC ']
                var17 = str(get_keyword(start, end, text))
                start1 = [' ']
                end1 = [' ']
                Quantity50 = get_keyword(start1, end1, var17)
                if Quantity50 is None:
                    # Search quantity50 on page 5
                    with pdfplumber.open(files) as pdf:
                        page = pdf.pages[4]
                        text = page.extract_text()
                        text = " ".join(text.split())
                        start = [' 50 ']
                        end = [' PC ']
                        var17 = str(get_keyword(start, end, text))
                        start1 = [' ']
                        end1 = [' ']
                        Quantity50 = get_keyword(start1, end1, var17)
                if Quantity50 is None:
                    # Search quantity50 on page 6
                    with pdfplumber.open(files) as pdf:
                        page = pdf.pages[5]
                        text = page.extract_text()
                        text = " ".join(text.split())
                        start = [' 50 ']
                        end = [' PC ']
                        var17 = str(get_keyword(start, end, text))
                        start1 = [' ']
                        end1 = [' ']
                        Quantity50 = get_keyword(start1, end1, var17)
            except IndexError:
                Quantity50 = "You don't have more items"

        # obtain key for : LeadTime50
        with pdfplumber.open(files) as pdf:
            try:
                page = pdf.pages[3]
                text = page.extract_text()
                text = " ".join(text.split())
                start = [' 50 ']
                end = [' 51 ']
                var7 = str(get_keyword(start, end, text))
                LeadTime50 = " "
                # IF YOU FIND SOMETHING ON PAGE  4
                if var7 != 'None':
                    start = [' Del. within : ']
                    end = [' 51 ']
                    LeadTime50 = str(get_keyword(start, end, var7))
                    # If the text does not end with 51, but with 'Q', we take Q as a reference
                    if len(LeadTime50) > 11:
                        start = [' Del. within : ']
                        end = [' Q']
                        LeadTime50 = str(get_keyword(start, end, var7))
                    # if the text does not end with 51, but with '30', we take 30 as a reference
                        if len(LeadTime50) > 11:
                            start = [' Del. within : ']
                            end = [' 51 ']
                            LeadTime50 = str(get_keyword(start, end, var7))

                    # WE HAVE ON PAGE4 ITEM 50, BUT DEL WITHIN IS ON PAGE 5
                    if LeadTime50 == 'None':
                        with pdfplumber.open(files) as pdf:
                            page = pdf.pages[4]
                            text = page.extract_text()
                            text = " ".join(text.split())
                            start = [' Del. within : ']
                            end = [' 51 ']
                            LeadTime50 = str(
                                get_keyword(start, end, text))

                # IF YOU FIND SOMETHING ON PAGE  5
                if var7 == 'None':
                    with pdfplumber.open(files) as pdf:
                        page = pdf.pages[4]
                        text = page.extract_text()
                        text = " ".join(text.split())
                        start = [' 50 ']
                        end = [' 51 ']
                        var7 = str(get_keyword(start, end, text))
                        if var7 != 'None':
                            start = [' Del. within : ']
                            end = [' 51 ']
                            LeadTime50 = str(get_keyword(start, end, var7))
                            # If the text does not end with 51, but with 'Q', we take Q as a reference
                            if len(LeadTime50) > 11:
                                start = [' Del. within : ']
                                end = [' Q']
                                LeadTime50 = str(
                                    get_keyword(start, end, var7))
                            # if the text does not end with 51, but with '30', we take 30 as a reference
                                if len(LeadTime50) > 11:
                                    start = [' Del. within : ']
                                    end = [' 50 ']
                                    LeadTime50 = str(
                                        get_keyword(start, end, var7))
                            # WE HAVE ON PAGE5 ITEM 40, BUT DEL WITHIN IS ON PAGE 6
                            if LeadTime50 == 'None':
                                with pdfplumber.open(files) as pdf:
                                    page = pdf.pages[5]
                                    text = page.extract_text()
                                    text = " ".join(text.split())
                                    start = [' Del. within : ']
                                    end = [' 51 ']
                                    LeadTime50 = str(
                                        get_keyword(start, end, text))
                # IF YOU FIND SOMETHING ON PAGE  6
                if var7 == 'None':
                    with pdfplumber.open(files) as pdf:
                        page = pdf.pages[5]
                        text = page.extract_text()
                        text = " ".join(text.split())
                        start = [' 50 ']
                        end = [' 51 ']
                        var7 = str(get_keyword(start, end, text))
                        if var7 != 'None':
                            start = [' Del. within : ']
                            end = [' 51 ']
                            LeadTime50 = str(get_keyword(start, end, var7))
                            # If the text does not end with 51, but with 'Q', we take Q as a reference
                            if len(LeadTime50) > 11:
                                start = [' Del. within : ']
                                end = [' Q']
                                LeadTime50 = str(
                                    get_keyword(start, end, var7))
                            # if the text does not end with 51, but with '30', we take 30 as a reference
                                if len(LeadTime50) > 11:
                                    start = [' Del. within : ']
                                    end = [' 50 ']
                                    LeadTime50 = str(get_keyword(
                                        start, end, var7))
                            # WE HAVE ON PAGE6 ITEM 50, BUT DEL WITHIN IS ON PAGE 7
                            if LeadTime50 == 'None':
                                with pdfplumber.open(files) as pdf:
                                    page = pdf.pages[7]
                                    text = page.extract_text()
                                    text = " ".join(text.split())
                                    start = [' Del. within : ']
                                    end = [' 51 ']
                                    LeadTime50 = str(
                                        get_keyword(start, end, text))
            except IndexError:
                LeadTime50 = "You don't have more items"

        # obtain key for : CostFromSupplier50
        with pdfplumber.open(files) as pdf:
            try:
                page = pdf.pages[3]
                text = page.extract_text()
                text = " ".join(text.split())
                start = [' 50 ']
                end = [' 51 ']
                var8 = str(get_keyword(start, end, text))
                CostFromSupplier50 = " "
                # IF YOU FIND SOMETHING ON PAGE  4
                if var8 != 'None':
                    start = [' PC 1 ']
                    end = ['A']
                    CostFromSupplier50 = str(get_keyword(start, end, var8))[:8]

                # IF YOU FIND SOMETHING ON PAGE  5
                if var8 == 'None':
                    with pdfplumber.open(files) as pdf:
                        page = pdf.pages[4]
                        text = page.extract_text()
                        text = " ".join(text.split())
                        start = [' 50 ']
                        end = [' 51 ']
                        var8 = str(get_keyword(start, end, text))
                        if var8 != 'None':
                            start = [' PC 1 ']
                            end = ['A']
                            CostFromSupplier50 = str(
                                get_keyword(start, end, var8))[:8]

                # IF YOU FIND SOMETHING ON PAGE  6
                if var8 == 'None':
                    with pdfplumber.open(files) as pdf:
                        page = pdf.pages[5]
                        text = page.extract_text()
                        text = " ".join(text.split())
                        start = [' 50 ']
                        end = [' 51 ']
                        var8 = str(get_keyword(start, end, text))
                        if var8 != 'None':
                            start = [' PC 1 ']
                            end = ['A']
                            CostFromSupplier50 = str(
                                get_keyword(start, end, var8))[:8]
            except IndexError:
                CostFromSupplier50 = "You don't have more items"

        # obtain key for : PartNumber60
        with pdfplumber.open(files) as pdf:
            try:
                page = pdf.pages[4]
                text = page.extract_text()
                text = " ".join(text.split())
                start = [' 60 ']
                end = [' ']
                PartNumber60 = get_keyword(start, end, text)
                if PartNumber60 == '000000':
                    start = [' 60 ']
                    end = ['..T']
                    PartNumber60 = str(get_keyword(start, end, text))[25:50]
                if PartNumber60 is None:
                    with pdfplumber.open(files) as pdf:
                        page = pdf.pages[5]
                        text = page.extract_text()
                        text = " ".join(text.split())
                        start = [' 60 ']
                        end = [' ']
                        PartNumber60 = get_keyword(start, end, text)
                        if PartNumber60 == '000000':
                            start = [' 60 ']
                            end = ['..T']
                            PartNumber60 = str(
                                get_keyword(start, end, text))[25:50]

                        if PartNumber60 is None:
                            with pdfplumber.open(files) as pdf:
                                page = pdf.pages[6]
                                text = page.extract_text()
                                text = " ".join(text.split())
                                start = [' 60 ']
                                end = [' ']
                                PartNumber60 = get_keyword(
                                    start, end, text)
                                if PartNumber60 == '000000':
                                    start = [' 60 ']
                                    end = ['..T']
                                    PartNumber60 = str(
                                        get_keyword(start, end, text))[25:50]
            except IndexError:
                PartNumber60 = "You don't have more items"

        # obtain key : Number of pieces Quantity60
        # Search quantity60 on page 5
        with pdfplumber.open(files) as pdf:
            try:
                page = pdf.pages[4]
                text = page.extract_text()
                text = " ".join(text.split())
                start = [' 60 ']
                end = [' PC ']
                var18 = str(get_keyword(start, end, text))
                start1 = [' ']
                end1 = [' ']
                Quantity60 = get_keyword(start1, end1, var18)
                if Quantity60 is None:
                    # Search quantity60 on page 6
                    with pdfplumber.open(files) as pdf:
                        page = pdf.pages[5]
                        text = page.extract_text()
                        text = " ".join(text.split())
                        start = [' 60 ']
                        end = [' PC ']
                        var18 = str(get_keyword(start, end, text))
                        start1 = [' ']
                        end1 = [' ']
                        Quantity60 = get_keyword(start1, end1, var18)
                if Quantity60 is None:
                    # Search quantity60 on page 7
                    with pdfplumber.open(files) as pdf:
                        page = pdf.pages[6]
                        text = page.extract_text()
                        text = " ".join(text.split())
                        start = [' 60 ']
                        end = [' PC ']
                        var18 = str(get_keyword(start, end, text))
                        start1 = [' ']
                        end1 = [' ']
                        Quantity60 = get_keyword(start1, end1, var18)
            except IndexError:
                Quantity60 = "You don't have more items"

        # obtain key for : LeadTime60
        with pdfplumber.open(files) as pdf:
            try:
                page = pdf.pages[4]
                text = page.extract_text()
                text = " ".join(text.split())
                start = [' 60 ']
                end = [' 61 ']
                var9 = str(get_keyword(start, end, text))
                LeadTime60 = " "
                # IF YOU FIND SOMETHING ON PAGE  5
                if var9 != 'None':
                    start = [' Del. within : ']
                    end = [' 61 ']
                    LeadTime60 = str(get_keyword(start, end, var9))
                    # If the text does not end with 61, but with 'Q', we take Q as a reference
                    if len(LeadTime60) > 11:
                        start = [' Del. within : ']
                        end = [' Q']
                        LeadTime60 = str(get_keyword(start, end, var9))
                    # if the text does not end with 61, but with '30', we take 30 as a reference
                        if len(LeadTime60) > 11:
                            start = [' Del. within : ']
                            end = [' 61 ']
                            LeadTime60 = str(get_keyword(start, end, var9))

                    # WE HAVE ON PAGE5 ITEM 60, BUT DEL WITHIN IS ON PAGE 6
                    if LeadTime60 == 'None':
                        with pdfplumber.open(files) as pdf:
                            page = pdf.pages[5]
                            text = page.extract_text()
                            text = " ".join(text.split())
                            start = [' Del. within : ']
                            end = [' 61 ']
                            LeadTime60 = str(
                                get_keyword(start, end, text))

                # IF YOU FIND SOMETHING ON PAGE  6
                if var9 == 'None':
                    with pdfplumber.open(files) as pdf:
                        page = pdf.pages[5]
                        text = page.extract_text()
                        text = " ".join(text.split())
                        start = [' 60 ']
                        end = [' 61 ']
                        var9 = str(get_keyword(start, end, text))
                        if var9 != 'None':
                            start = [' Del. within : ']
                            end = [' 61 ']
                            LeadTime60 = str(get_keyword(start, end, var9))
                            # If the text does not end with 61, but with 'Q', we take Q as a reference
                            if len(LeadTime60) > 11:
                                start = [' Del. within : ']
                                end = [' Q']
                                LeadTime60 = str(
                                    get_keyword(start, end, var9))
                            # if the text does not end with 61, but with '30', we take 30 as a reference
                                if len(LeadTime60) > 11:
                                    start = [' Del. within : ']
                                    end = [' 60 ']
                                    LeadTime60 = str(
                                        get_keyword(start, end, var9))
                            # WE HAVE ON PAGE6 ITEM 40, BUT DEL WITHIN IS ON PAGE 7
                            if LeadTime60 == 'None':
                                with pdfplumber.open(files) as pdf:
                                    page = pdf.pages[6]
                                    text = page.extract_text()
                                    text = " ".join(text.split())
                                    start = [' Del. within : ']
                                    end = [' 61 ']
                                    LeadTime60 = str(
                                        get_keyword(start, end, text))
                # IF YOU FIND SOMETHING ON PAGE  7
                if var9 == 'None':
                    with pdfplumber.open(files) as pdf:
                        page = pdf.pages[6]
                        text = page.extract_text()
                        text = " ".join(text.split())
                        start = [' 60 ']
                        end = [' 61 ']
                        var9 = str(get_keyword(start, end, text))
                        if var9 != 'None':
                            start = [' Del. within : ']
                            end = [' 61 ']
                            LeadTime60 = str(get_keyword(start, end, var9))
                            # If the text does not end with 61, but with 'Q', we take Q as a reference
                            if len(LeadTime60) > 11:
                                start = [' Del. within : ']
                                end = [' Q']
                                LeadTime60 = str(
                                    get_keyword(start, end, var9))
                            # if the text does not end with 61, but with '30', we take 30 as a reference
                                if len(LeadTime60) > 11:
                                    start = [' Del. within : ']
                                    end = [' 60 ']
                                    LeadTime60 = str(get_keyword(
                                        start, end, var9))
                            # WE HAVE ON PAGE7 ITEM 40, BUT DEL WITHIN IS ON PAGE 8
                            if LeadTime60 == 'None':
                                with pdfplumber.open(files) as pdf:
                                    page = pdf.pages[7]
                                    text = page.extract_text()
                                    text = " ".join(text.split())
                                    start = [' Del. within : ']
                                    end = [' 61 ']
                                    LeadTime60 = str(
                                        get_keyword(start, end, text))
            except IndexError:
                LeadTime60 = "You don't have more items"

        # obtain key for : CostFromSupplier60
        with pdfplumber.open(files) as pdf:
            try:
                page = pdf.pages[4]
                text = page.extract_text()
                text = " ".join(text.split())
                start = [' 60 ']
                end = [' 61 ']
                var10 = str(get_keyword(start, end, text))
                CostFromSupplier60 = " "
                # IF YOU FIND SOMETHING ON PAGE  5
                if var10 != 'None':
                    start = [' PC 1 ']
                    end = ['A']
                    CostFromSupplier60 = str(
                        get_keyword(start, end, var10))[:8]

                # IF YOU FIND SOMETHING ON PAGE  6
                if var10 == 'None':
                    with pdfplumber.open(files) as pdf:
                        page = pdf.pages[5]
                        text = page.extract_text()
                        text = " ".join(text.split())
                        start = [' 60 ']
                        end = [' 61 ']
                        var10 = str(get_keyword(start, end, text))
                        if var10 != 'None':
                            start = [' PC 1 ']
                            end = ['A']
                            CostFromSupplier60 = str(
                                get_keyword(start, end, var10))[:8]

                # IF YOU FIND SOMETHING ON PAGE  7
                if var10 == 'None':
                    with pdfplumber.open(files) as pdf:
                        page = pdf.pages[6]
                        text = page.extract_text()
                        text = " ".join(text.split())
                        start = [' 60 ']
                        end = [' 61 ']
                        var10 = str(get_keyword(start, end, text))
                        if var10 != 'None':
                            start = [' PC 1 ']
                            end = ['A']
                            CostFromSupplier60 = str(
                                get_keyword(start, end, var10))[:8]
            except IndexError:
                CostFromSupplier60 = "You don't have more items"

        # obtain key for : PartNumber70
        # SEARCH PartNumber70 ON PAGE 5
        with pdfplumber.open(files) as pdf:
            try:
                page = pdf.pages[4]
                text = page.extract_text()
                text = " ".join(text.split())
                start = [' 70 ']
                end = [' ']
                PartNumber70 = get_keyword(start, end, text)
                if PartNumber70 == '000000':
                    start = [' 70 ']
                    end = ['..T']
                    PartNumber70 = str(get_keyword(start, end, text))[25:50]
                # SEARCH PartNumber70 ON PAGE 6
                if PartNumber70 is None:
                    with pdfplumber.open(files) as pdf:
                        page = pdf.pages[5]
                        text = page.extract_text()
                        text = " ".join(text.split())
                        start = [' 70 ']
                        end = [' ']
                        PartNumber70 = get_keyword(start, end, text)
                        if PartNumber70 == '000000':
                            start = [' 70 ']
                            end = ['..T']
                            PartNumber70 = str(
                                get_keyword(start, end, text))[25:50]
                        # SEARCH PartNumber70 ON PAGE 7
                        if PartNumber70 is None:
                            with pdfplumber.open(files) as pdf:
                                page = pdf.pages[6]
                                text = page.extract_text()
                                text = " ".join(text.split())
                                start = [' 70 ']
                                end = [' ']
                                PartNumber70 = get_keyword(
                                    start, end, text)
                                if PartNumber70 == '000000':
                                    start = [' 70 ']
                                    end = ['..T']
                                    PartNumber70 = str(
                                        get_keyword(start, end, text))[25:50]
                                # SEARCH PartNumber70 ON PAGE 8
                                if PartNumber70 is None:
                                    with pdfplumber.open(files) as pdf:
                                        page = pdf.pages[7]
                                        text = page.extract_text()
                                        text = " ".join(
                                            text.split())
                                        start = [' 70 ']
                                        end = [' ']
                                        PartNumber70 = get_keyword(
                                            start, end, text)
                                        if PartNumber70 == '000000':
                                            start = [' 70 ']
                                            end = ['..T']
                                            PartNumber70 = str(
                                                get_keyword(start, end, text))[25:50]
            except IndexError:
                PartNumber70 = "You don't have more items"

        # obtain key : Number of pieces Quantity70
        # Search quantity70 on page 5
        with pdfplumber.open(files) as pdf:
            try:
                page = pdf.pages[4]
                text = page.extract_text()
                text = " ".join(text.split())
                start = [' 70 ']
                end = [' PC ']
                var19 = str(get_keyword(start, end, text))
                start1 = [' ']
                end1 = [' ']
                Quantity70 = get_keyword(start1, end1, var19)
                if Quantity70 is None:
                    # Search quantity70 on page 6
                    with pdfplumber.open(files) as pdf:
                        page = pdf.pages[5]
                        text = page.extract_text()
                        text = " ".join(text.split())
                        start = [' 70 ']
                        end = [' PC ']
                        var19 = str(get_keyword(start, end, text))
                        start1 = [' ']
                        end1 = [' ']
                        Quantity70 = get_keyword(start1, end1, var19)
                if Quantity70 is None:
                    # Search quantity70 on page 7
                    with pdfplumber.open(files) as pdf:
                        page = pdf.pages[6]
                        text = page.extract_text()
                        text = " ".join(text.split())
                        start = [' 70 ']
                        end = [' PC ']
                        var19 = str(get_keyword(start, end, text))
                        start1 = [' ']
                        end1 = [' ']
                        Quantity70 = get_keyword(start1, end1, var19)
                if Quantity70 is None:
                    # Search quantity70 on page 8
                    with pdfplumber.open(files) as pdf:
                        page = pdf.pages[7]
                        text = page.extract_text()
                        text = " ".join(text.split())
                        start = [' 70 ']
                        end = [' PC ']
                        var19 = str(get_keyword(start, end, text))
                        start1 = [' ']
                        end1 = [' ']
                        Quantity70 = get_keyword(start1, end1, var19)
            except IndexError:
                Quantity70 = "You don't have more items"

        # obtain key for : LeadTime70
        # SEARCH LeadTime70 ON PAGE 56
        with pdfplumber.open(files) as pdf:
            try:
                page = pdf.pages[4]
                text = page.extract_text()
                text = " ".join(text.split())
                start = [' 70 ']
                end = [' 71 ']
                var11 = str(get_keyword(start, end, text))
                LeadTime70 = " "
                # IF YOU FIND SOMETHING ON PAGE  6
                if var11 != 'None':
                    start = [' Del. within : ']
                    end = [' 71 ']
                    LeadTime70 = str(get_keyword(start, end, var11))
                    # If the text does not end with 71, but with 'Q', we take Q as a reference
                    if len(LeadTime70) > 11:
                        start = [' Del. within : ']
                        end = [' Q']
                        LeadTime70 = str(get_keyword(start, end, var11))
                    # if the text does not end with 71, but with '30', we take 30 as a reference
                        if len(LeadTime70) > 11:
                            start = [' Del. within : ']
                            end = [' 71 ']
                            LeadTime70 = str(get_keyword(start, end, var11))

                    # WE HAVE ON PAGE6 ITEM 70, BUT DEL WITHIN IS ON PAGE 7
                    if LeadTime70 == 'None':
                        with pdfplumber.open(files) as pdf:
                            page = pdf.pages[5]
                            text = page.extract_text()
                            text = " ".join(text.split())
                            start = [' Del. within : ']
                            end = [' 71 ']
                            LeadTime70 = str(
                                get_keyword(start, end, text))

                # IF YOU FIND SOMETHING ON PAGE  7
                if var11 == 'None':
                    with pdfplumber.open(files) as pdf:
                        page = pdf.pages[5]
                        text = page.extract_text()
                        text = " ".join(text.split())
                        start = [' 70 ']
                        end = [' 71 ']
                        var11 = str(get_keyword(start, end, text))
                        if var11 != 'None':
                            start = [' Del. within : ']
                            end = [' 71 ']
                            LeadTime70 = str(
                                get_keyword(start, end, var11))
                            # If the text does not end with 71, but with 'Q', we take Q as a reference
                            if len(LeadTime70) > 11:
                                start = [' Del. within : ']
                                end = [' Q']
                                LeadTime70 = str(
                                    get_keyword(start, end, var11))
                            # if the text does not end with 71, but with '30', we take 30 as a reference
                                if len(LeadTime70) > 11:
                                    start = [' Del. within : ']
                                    end = [' 70 ']
                                    LeadTime70 = str(
                                        get_keyword(start, end, var11))
                            # WE HAVE ON PAGE7 ITEM 70, BUT DEL WITHIN IS ON PAGE 8
                            if LeadTime70 == 'None':
                                with pdfplumber.open(files) as pdf:
                                    page = pdf.pages[6]
                                    text = page.extract_text()
                                    text = " ".join(text.split())
                                    start = [' Del. within : ']
                                    end = [' 71 ']
                                    LeadTime70 = str(
                                        get_keyword(start, end, text))

                # IF YOU FIND SOMETHING ON PAGE  8
                if var11 == 'None':
                    with pdfplumber.open(files) as pdf:
                        page = pdf.pages[6]
                        text = page.extract_text()
                        text = " ".join(text.split())
                        start = [' 70 ']
                        end = [' 71 ']
                        var11 = str(get_keyword(start, end, text))
                        if var11 != 'None':
                            start = [' Del. within : ']
                            end = [' 71 ']
                            LeadTime70 = str(
                                get_keyword(start, end, var11))
                            # If the text does not end with 71, but with 'Q', we take Q as a reference
                            if len(LeadTime70) > 11:
                                start = [' Del. within : ']
                                end = [' Q']
                                LeadTime70 = str(
                                    get_keyword(start, end, var11))
                            # if the text does not end with 71, but with '30', we take 30 as a reference
                                if len(LeadTime70) > 11:
                                    start = [' Del. within : ']
                                    end = [' 70 ']
                                    LeadTime70 = str(get_keyword(
                                        start, end, var11))
                            # WE HAVE ON PAGE8 ITEM 70, BUT DEL WITHIN IS ON PAGE 9
                            if LeadTime70 == 'None':
                                with pdfplumber.open(files) as pdf:
                                    page = pdf.pages[7]
                                    text = page.extract_text()
                                    text = " ".join(text.split())
                                    start = [' Del. within : ']
                                    end = [' 71 ']
                                    LeadTime70 = str(
                                        get_keyword(start, end, text))

                if var11 == 'None':
                    with pdfplumber.open(files) as pdf:
                        page = pdf.pages[7]
                        text = page.extract_text()
                        text = " ".join(text.split())
                        start = [' 70 ']
                        end = [' 71 ']
                        var11 = str(get_keyword(start, end, text))
                        if var11 != 'None':
                            start = [' Del. within : ']
                            end = [' 71 ']
                            LeadTime70 = str(
                                get_keyword(start, end, var11))
                            # If the text does not end with 71, but with 'Q', we take Q as a reference
                            if len(LeadTime70) > 11:
                                start = [' Del. within : ']
                                end = [' Q']
                                LeadTime70 = str(
                                    get_keyword(start, end, var11))
                                # if the text does not end with 71, but with '30', we take 30 as a reference
                                if len(LeadTime70) > 11:
                                    start = [' Del. within : ']
                                    end = [' 70 ']
                                    LeadTime70 = str(
                                        get_keyword(start, end, var11))
                            # WE HAVE ON PAGE8 ITEM 70, BUT DEL WITHIN IS ON PAGE 9
                            if LeadTime70 == 'None':
                                with pdfplumber.open(files) as pdf:
                                    page = pdf.pages[8]
                                    text = page.extract_text()
                                    text = " ".join(text.split())
                                    start = [' Del. within : ']
                                    end = [' 71 ']
                                    LeadTime70 = str(
                                        get_keyword(start, end, text))
            except IndexError:
                LeadTime70 = "You don't have more items"

        # obtain key for : CostFromSupplier70
        with pdfplumber.open(files) as pdf:
            try:
                page = pdf.pages[4]
                text = page.extract_text()
                text = " ".join(text.split())
                start = [' 70 ']
                end = [' 71 ']
                var12 = str(get_keyword(start, end, text))
                CostFromSupplier70 = " "
                # IF YOU FIND SOMETHING ON PAGE  5
                if var12 != 'None':
                    start = [' PC 1 ']
                    end = ['A']
                    CostFromSupplier70 = str(
                        get_keyword(start, end, var12))[:8]

                # IF YOU FIND SOMETHING ON PAGE  7
                if var12 == 'None':
                    with pdfplumber.open(files) as pdf:
                        page = pdf.pages[5]
                        text = page.extract_text()
                        text = " ".join(text.split())
                        start = [' 70 ']
                        end = [' 71 ']
                        var12 = str(get_keyword(start, end, text))
                        if var12 != 'None':
                            start = [' PC 1 ']
                            end = ['A']
                            CostFromSupplier70 = str(
                                get_keyword(start, end, var12))[:8]

                # IF YOU FIND SOMETHING ON PAGE  8
                if var12 == 'None':
                    with pdfplumber.open(files) as pdf:
                        page = pdf.pages[6]
                        text = page.extract_text()
                        text = " ".join(text.split())
                        start = [' 70 ']
                        end = [' 71 ']
                        var12 = str(get_keyword(start, end, text))
                        if var12 != 'None':
                            start = [' PC 1 ']
                            end = ['A']
                            CostFromSupplier70 = str(
                                get_keyword(start, end, var12))[:8]

                if var12 == 'None':
                    with pdfplumber.open(files) as pdf:
                        page = pdf.pages[7]
                        text = page.extract_text()
                        text = " ".join(text.split())
                        start = [' 70 ']
                        end = [' 71 ']
                        var12 = str(get_keyword(start, end, text))
                        if var12 != 'None':
                            start = [' PC 1 ']
                            end = ['A']
                            CostFromSupplier70 = str(
                                get_keyword(start, end, var12))[:8]
            except IndexError:
                CostFromSupplier70 = "You don't have more items"

            if PartNumber20 is None:
                PartNumber20 = "You don't have more items"
                Quantity20 = "You don't have more items"
                LeadTime20 = "You don't have more items"
                CostFromSupplier20 = "You don't have more items"
            if PartNumber30 is None:
                PartNumber30 = "You don't have more items"
                Quantity30 = "You don't have more items"
                LeadTime30 = "You don't have more items"
                CostFromSupplier30 = "You don't have more items"
            if PartNumber40 is None:
                PartNumber40 = "You don't have more items"
                Quantity40 = "You don't have more items"
                LeadTime40 = "You don't have more items"
                CostFromSupplier40 = "You don't have more items"
            if PartNumber50 is None:
                PartNumber50 = "You don't have more items"
                Quantity50 = "You don't have more items"
                LeadTime50 = "You don't have more items"
                CostFromSupplier50 = "You don't have more items"
            if PartNumber60 is None:
                PartNumber60 = "You don't have more items"
                Quantity60 = "You don't have more items"
                LeadTime60 = "You don't have more items"
                CostFromSupplier60 = "You don't have more items"
            if PartNumber70 is None:
                PartNumber70 = "You don't have more items"
                Quantity70 = "You don't have more items"
                LeadTime70 = "You don't have more items"
                CostFromSupplier70 = "You don't have more items"

        # append my list as a row in the dataframe
        df = pd.DataFrame({'PartNumbers': [PartNumber, PartNumber20, PartNumber30, PartNumber40, PartNumber50, PartNumber60, PartNumber70],
                           'CostFromSupplier': [CostFromSupplier, CostFromSupplier20, CostFromSupplier30, CostFromSupplier40, CostFromSupplier50, CostFromSupplier60, CostFromSupplier70],
                           'TotalQuantity': [Quantity, Quantity20, Quantity30, Quantity40, Quantity50, Quantity60, Quantity70],
                           'LeadTime': [LeadTime, LeadTime20, LeadTime30, LeadTime40, LeadTime50, LeadTime60, LeadTime70],
                           'Currency': [Currency, Currency, Currency, Currency, Currency, Currency, Currency],
                           'PriceValidity': [PriceValidity, PriceValidity, PriceValidity, PriceValidity, PriceValidity, PriceValidity, PriceValidity],
                           'SupplierQuote': [SupplierQuote, SupplierQuote, SupplierQuote, SupplierQuote, SupplierQuote, SupplierQuote, SupplierQuote],
                           'Supplier': [Supplier, Supplier, Supplier, Supplier, Supplier, Supplier, Supplier]})

        # append the list of items as row to my dataframe
        my_dataframe = my_dataframe.append(
            df, ignore_index=True)

    # change my currnet working directory
        save_path = (r'C:\Users\E1328977\Desktop\Robocorp-trainingprojects\Robocorp-trainingprojects\MSOL_682_Supplier_Price_validity_log_for_Manifolds\MSOL_682_robo_py')
        os.chdir(save_path)

    # extract my dataframe to an .xlsx file
        my_dataframe.to_excel('sample_excel.xlsx', sheet_name='my_dataframe')
        print("")
        print(my_dataframe)


if __name__ == '__main__':
    main()

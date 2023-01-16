import pdfplumber
import pandas as pd
import glob
import os


def get_keyword(start, end, text):
    """PDF
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
    # Change the file where the pdfs are, leaving only " \*.pdf " at the end!!!
    for files in glob.glob(r"C:\Users\E1328977\Desktop\OviPDF\*.pdf"):
        with pdfplumber.open(files) as pdf:
            page = pdf.pages[0]
            text = page.extract_text()
            text = " ".join(text.split())

    # obtain key for : PROJECT
            start = [' Project: ']
            end = [' Project']
            Project = get_keyword(start, end, text)

    # obtain key for : TagNo.
            start = ['No. ']
            end = [' 42 ']
            TagNo = get_keyword(start, end, text)

    # obtain key : Fluid State at Inlet
            start = [' Fluid State at Inlet ']
            end = [' 5 ']
            FluidStateAndInlet = get_keyword(start, end, text)
            if FluidStateAndInlet is None:
                start = ['FluidStateatInlet ']
                end = [' 5 ']
                FluidStateAndInlet = get_keyword(start, end, text)

    # obtain key : Fluid Name
            start = ['Name ']
            end = [' 8 ']
            FluidName = get_keyword(start, end, text)

    # obtain key : Inlet
            start = ['12 Inlet ']
            end = ['52']
            Inlet = get_keyword(start, end, text)

    # obtain key : Outlet
            start = ['13 Outlet ']
            end = ['53']
            Outlet = get_keyword(start, end, text)

    # obtain key : Spring
            start = ['Spring ']
            end = [' 6']
            Spring = get_keyword(start, end, text)

    # obtain key : CDTP
            start = ['CDTP ']
            end = ['c']
            CDTP = get_keyword(start, end, text)

    # obtain key : Constant Superimposed
            start = ['Constant Superimposed ']
            end = [' ']
            ConstantSuperimposed = get_keyword(start, end, text)
            if ConstantSuperimposed is None:
                start = ['ConstantSuperimposed ']
                end = [' ']
                ConstantSuperimposed = get_keyword(start, end, text)

    # obtain key : Variable Superimposed
            start = ['Variable Superimposed ']
            end = [' ']
            VariableSuperimposed = get_keyword(start, end, text)
            if VariableSuperimposed is None:
                start = ['VariableSuperimposed ']
                end = [' ']
                VariableSuperimposed = get_keyword(start, end, text)

    # obtain key : Relieving
            start = ['Operating Relieving ']
            end = [' ']
            Relieving = get_keyword(start, end, text)

    # obtain key : API
            start = ['Orifice ']
            end = ['75']
            Orifice = get_keyword(start, end, text)

    # create a list with keywords extracted from pdf's
            List_keywords = [Project, TagNo,
                             FluidStateAndInlet, FluidName, Inlet, Outlet, Spring, CDTP, ConstantSuperimposed, VariableSuperimposed, Relieving, Orifice]

    # append my list as a row in the dataframe
            List_keywords = pd.Series(List_keywords)

        # append the list of items as row to my dataframe
            my_dataframe = my_dataframe.append(
                List_keywords, ignore_index=True)

# rename dataframe columns using dictionaries
    my_dataframe = my_dataframe.rename(columns={0: 'PROJECT',
                                                1: 'TAG_NO.',
                                                2: 'FLUID_STATE_AND_INLET',
                                                3: 'FLUID_NAME',
                                                4: 'INLET',
                                                5: 'OUTLET',
                                                6: 'SPRING',
                                                7: 'CDTP',
                                                8: 'CONSTANT_SUPERIMPOSED',
                                                9: 'VARIABLE_SUPERIMPOSED',
                                                10: 'RELIEVING',
                                                11: 'ORIFICE'})

# change my currnet working directory !!!
    save_path = (r'C:\Users\E1328977\Desktop\Robocorp-trainingprojects\Robocorp-trainingprojects\MSOL_682_Supplier_Price_validity_log_for_Manifolds\MSOL_682_robo_py')
    os.chdir(save_path)

# extract my dataframe to an .xslx file !!!
    my_dataframe.to_excel('sample_excel.xlsx', sheet_name='my_dataframe')
    print(my_dataframe)


if __name__ == '__main__':
    main()

import PyPDF2

pdf_path = '数据pdf.pdf'

def print_pdf_text(pdf_path, max_pages=3):
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for i, page in enumerate(reader.pages):
            if i >= max_pages:
                break
            text = page.extract_text()
            print(f'--- 第{i+1}页内容 ---')
            print(text)
            print('\n')

if __name__ == '__main__':
    print_pdf_text(pdf_path)

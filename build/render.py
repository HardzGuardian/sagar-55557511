from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome',args=['--no-sandbox'])
    pg=b.new_page(); pg.goto('file:///home/user/sagar-55557511/build/guide.html')
    pg.pdf(path='AI_Exam_Answer_Guide.pdf',format='A4',print_background=True,margin=dict(top='16mm',bottom='16mm',left='14mm',right='14mm'),display_header_footer=True,footer_template='<div style="font-size:8px;width:100%;text-align:center;color:#777"><span class="pageNumber"></span> / <span class="totalPages"></span></div>',header_template='<div></div>')
    b.close()

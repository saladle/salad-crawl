# Import the sync_playwright function from the sync_api module of Playwright.
from playwright.sync_api import sync_playwright


# ----- CONFIG -----
cssLinkList = [
    '//static1.asdxstatic.com/web/pc/static/ssr/5d10f0af22fc52d5b279.css',
    '//static1.asdxstatic.com/web/pc/static/ssr/bb539c73d744775fd032.css',
    '//static1.asdxstatic.com/web/pc/static/ssr/648f434e2d90e78e08fe.css',
    '//static1.asdxstatic.com/web/pc/static/ssr/efe8353351aea64b6bc5.css',
]
websiteName = "AscendEX"
maximumLinksAtOnce = 12
# maximumLinksAtOnce = 20
# ------------------

# Start a new session with Playwright using the sync_playwright function.
with sync_playwright() as playwright:
    # Kết nối tới trình duyệt đang mở sẵn với debug port 9222
    browser = playwright.chromium.connect_over_cdp("http://localhost:9222")

    # Retrieve the first context of the browser.
    default_context = browser.contexts[0]

    # Sử dụng page đầu tiên trong trình duyệt
    page = default_context.pages[0]

    # page = browser.new_page()

    # Begin: Lấy list CSS
    print("Đang tìm kiếm link css...")
    page.goto("https://ascendex.com/en/global-digital-asset-platform")
    css_link_elements = page.query_selector_all('link[rel="stylesheet"]')

    cssLinkList = [element.get_attribute('href')
                   for element in css_link_elements]
    numberOfLinks = len(cssLinkList)
    remainCount = numberOfLinks

    print("Đã hoàn thành tìm kiếm " + str(len(cssLinkList)) + " link css")
    # End: Lấy list CSS

    # Di chuyển đến trang google ads
    print("Đang khởi tạo quá trình điền link...")
    page.goto(
        "https://ads.google.com/aw/assetreport/associations/sitelink?ocid=1131763371")
    while remainCount > 0:        
        # Ấn vào dấu cộng
        # addButtonElement = page.wait_for_selector('.content._ngcontent-awn-CM-37')
        addButtonElement = page.wait_for_selector(
            '._ngcontent-awn-CM-29._nghost-awn-CM-30')
        addButtonElement.click()
        page.wait_for_load_state()

        print("Đang thực hiện điền link css từ link thứ " +
              str(numberOfLinks-remainCount + 1))

        # Chọn option Thêm vào "Nhóm quảng cáo"
        selectButtonElement = page.wait_for_selector(
            '.button._ngcontent-awn-CM_EDITING-23')
        selectButtonElement.click()
        page.wait_for_load_state()
        option3Element = page.wait_for_selector(
            '.item._nghost-awn-CM_EDITING-40._ngcontent-awn-CM_EDITING-22:nth-child(3)')
        option3Element.click()
        page.wait_for_load_state()

        # Chọn Website traffic-Search-1
        campaignElement = page.wait_for_selector(
            '.particle-table-row.particle-table-last-row')
        campaignElement.click()
        page.wait_for_load_state()

        # Chọn Nhóm quảng cáo 1
        adsGroupElement = page.wait_for_selector('.tools-cell')
        adsGroupElement.click()
        page.wait_for_load_state()

        # click vào nút "Xong"
        completeButtonElement = page.wait_for_selector('#picker-save-button')
        completeButtonElement.click()
        page.wait_for_load_state()

        # Mở các tab nhập linh 2, 3, 4 đang bị đóng
        webOptionElements = page.query_selector_all(
            '.main-header._ngcontent-awn-CM_EDITING-36')
        for i in range(3):
            webOptionElements[i + 1].click()
        page.wait_for_load_state()

        # Mở hết tất cả 20 tab nhập link
        for i in range(maximumLinksAtOnce - 4):
            addLinkElement = page.wait_for_selector(
                '.content._ngcontent-awn-CM_EDITING-9')
            addLinkElement.click()
            page.wait_for_load_state()

        # Lấy hết tất cả 80 ô input hiện có
        inputElements = page.query_selector_all(
            '.input.input-area._ngcontent-awn-CM_EDITING-33')

        # Kiểm tra số link còn lại cần nhập
        if remainCount >= maximumLinksAtOnce:
            loop_range = maximumLinksAtOnce
        else:
            loop_range = remainCount

        # Điền các tên và link vào các ô input
        for i in range(loop_range):
            # input_index = 4*(numberOfLinks-remainCount)
            link_index = numberOfLinks-remainCount
            inputElements[4 * i].fill(
                websiteName + " " + str(link_index + 1))
            inputElements[4 * i + 3].fill("https:" + cssLinkList[link_index])
            remainCount = remainCount - 1
            page.wait_for_load_state()

        # Ấn nút lưu
        saveButtonElement = page.wait_for_selector(
            '.btn.btn-yes._nghost-awn-CM_EDITING-9._ngcontent-awn-CM_EDITING-7.highlighted')
        saveButtonElement.click()
        page.wait_for_load_state()
        # Ấn nút tiếp tục
        continueButtonElement = page.query_selector_all(
            '.content._ngcontent-awn-CM_EDITING-9')
        continueButtonElement[5].click()
        page.wait_for_load_state()

    # # Nhập tên web 1
    # web1NameInputElement = page.wait_for_selector('.input.input-area._ngcontent-awn-CM_EDITING-33')
    # print(web1NameInputElement.text_content())
    # web1NameInputElement.fill(f"{websiteName} 1")
    # page.wait_for_load_state()
    # # Nhập link 1
    # web1LinkInputButtonElement = page.query_selector_all('.input.input-area._ngcontent-awn-CM_EDITING-33')
    # # web1LinkInputButtonElement[3].fill(cssLinkList[0])
    # web1LinkInputButtonElement[3].fill("https:" + cssLinkList[0])
    # page.wait_for_load_state()

    # # Nhập tên web 2
    # web2NameInputElement = page.query_selector_all('.input.input-area._ngcontent-awn-CM_EDITING-33')
    # web2NameInputElement[4].fill(f"{websiteName} 2")
    # page.wait_for_load_state()
    # # Nhập link 2
    # # web2LinkInputButtonElement = page.wait_for_selector('')
    # # web2NameInputElement[7].fill(cssLinkList[1])
    # web2NameInputElement[7].fill("https:" + cssLinkList[1])
    # page.wait_for_load_state()

    # # Nhập tên web 3
    # web3NameInputElement = page.query_selector_all('.input.input-area._ngcontent-awn-CM_EDITING-33')
    # web3NameInputElement[8].fill(f"{websiteName} 3")
    # page.wait_for_load_state()
    # # Nhập link 3
    # # web3NameInputElement[11].fill(cssLinkList[2])
    # web3NameInputElement[11].fill("https:" + cssLinkList[2])
    # page.wait_for_load_state()

    # # Nhập tên web 4
    # web4NameInputElement = page.query_selector_all('.input.input-area._ngcontent-awn-CM_EDITING-33')
    # web4NameInputElement[12].fill(f"{websiteName} 4")
    # page.wait_for_load_state()
    # # Nhập link 4
    # # web4NameInputElement[15].fill(cssLinkList[3])
    # web4NameInputElement[15].fill("https:" + cssLinkList[3])
    # page.wait_for_load_state()

    # # Mở hết tất cả 20 tab nhập link
    # for i in range(16):
    #     addLinkElement = page.wait_for_selector('.content._ngcontent-awn-CM_EDITING-9')
    #     addLinkElement.click()
    #     page.wait_for_load_state()

    # # Ấn nút lưu
    # saveButtonElement = page.wait_for_selector('.btn.btn-yes._nghost-awn-CM_EDITING-9._ngcontent-awn-CM_EDITING-7.highlighted')
    # saveButtonElement.click()
    # page.wait_for_load_state()
    # # Ấn nút tiếp tục
    # continueButtonElement = page.query_selector_all('.content._ngcontent-awn-CM_EDITING-9')
    # continueButtonElement[5].click()
    # page.wait_for_load_state()
    # End

    page.screenshot(path="demo2.png")
    # Print the title of the page.
    print(page.title())

    # Print the URL of the page.
    print(page.url)

    browser.close()

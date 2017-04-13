from Common.downloader import Downloader


def basicFRDownload(pUrl='', pK_code='', pMarket='', pTypes=['lrb', 'fzb', 'llb'], pCode='', pOrgid='', pMinYear='',
                    pMaxYear='', pHq_code='', pHq_k_code='', pCw_code='', pCw_k_code=''):
    for frtype in pTypes:
        values = {
            'K_code': pK_code,
            'market': pMarket,  # Required
            'type': frtype,  # Required
            'code': pCode,  # Required
            'orgid': pOrgid,  # Required
            'minYear': pMinYear,  # Required
            'maxYear': pMaxYear,  # Required
            'hq_code': pHq_code,
            'hq_k_code': pHq_k_code,
            'cw_code': pCw_code,  # Required
            'cw_k_code': pCw_k_code
        }
        D = Downloader()
        D.data = values
        D.saveZipToLocal(pUrl, extract=True)


def getFR(url='', stock_list=[], types=['lrb', 'fzb', 'llb']):
    """
    stock_list = [[stock_code, minYear, maxYear]]
    """
    for stock in stock_list:
        if stock[0] < '599999':
            market = 'sz'
            orgid = 'gssz' + stock[0]
        else:
            market = 'sh'
            orgid = 'gssh' + stock[0]
        basicFRDownload(pUrl=url, pMarket=market, pTypes=types, pCode=stock[0], pOrgid=orgid, pMinYear=stock[1],
                        pMaxYear=stock[2], pCw_code=stock[0])

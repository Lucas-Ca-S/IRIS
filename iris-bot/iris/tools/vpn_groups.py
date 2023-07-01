def get_vpn_groups(product:str):
    groups = {
        'RH': [
            {
                'name':'LNC-RH',
                'value':'3722e96ed4478ye39a023693'
            }
        ],
        'Desenvolvimento': [
            {
                'name':'LNC-PRODUCTION',
                'value':'63344428ed474835bfa7e473'
            },
            {
                'name':'LNC-PLATFORM',
                'value':'32q28s6f3e3e9c54bf7ac203'
            }
        ],
        'QA':[
            {
                'name':'LNC-QA',
                'value':'6400e37ey477336sfa0097b4'
            }
        ]
    }
    return groups[product]
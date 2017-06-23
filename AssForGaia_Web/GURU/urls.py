from django.conf.urls import url
from GURU import updateLogin,updateWebSource,main,GAIAPAYROLL

urlpatterns = [
    url(r'^$',main.main),
    url(r'^main/updateLogin$',updateLogin.loginConfig),
    url(r'^main/saveNewConnecttion/$', updateLogin.saveNewConnecttion, name='saveNewConnecttion'),
    url(r'^main/updateWebSource$',updateWebSource.websourceConfig),
    url(r'^main/saveWebSource/$', updateWebSource.saveWebSource, name='saveWebSource'),
    url(r'^main/$',main.main),
    url(r'^GAIAPAYROLL/$',GAIAPAYROLL.GAIAPAYROLL),
    url(r'^GAIAPAYROLL/updatePayroll/$',GAIAPAYROLL.web_updatePublicGroupByDoc),
    url(r'^GAIAPAYROLL/updateFormuAbout/$',GAIAPAYROLL.web_updateFormuAbout),
    url(r'^GAIAPAYROLL/updateInsAbout/$',GAIAPAYROLL.web_updateInsAbout),
    url(r'^GAIAPAYROLL/updatePYCALAbout/$',GAIAPAYROLL.web_payrollCal),
    
    url(r'^GAIAPAYROLLCAL/$',GAIAPAYROLL.web_GAIAPAYROLLCAL),
    url(r'^GAIAPAYROLLCAL/updatePYCALAbout/$',GAIAPAYROLL.web_payrollCal),
    


   
]
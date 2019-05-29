const puppeteer = require('puppeteer');
const request = require('request');


module.exports = () => {


    fssp_parse.checkCapcha = (page, timioutCheckCapcha = 20000) {
        return new Promise((resolve, reject) => {
          setTimeout(async function() {

            console.log("[i] Testing page after "+timioutCheckCapcha+" sec ")

            let r = await page.evaluate(function() {
              var res = {err: '', content: '', status: 403}
              if($('.t-capcha').length > 0){
                console.log("[i] Capcha is detected.");
                res['err'] = "Capcha is detected";
                res['content'] = $('.context img').attr('src');
                return res
              }
              res['content'] = $('body').html()
              res['status'] = 200
              return res
            })
            resolve(r)
          }, timioutCheckCapcha);
        }).catch((e) => {console.log(e);})
    }

    return fssp_parse
}
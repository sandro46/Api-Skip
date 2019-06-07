

const puppeteer = require('puppeteer');
const request = require('request');

const proxyAddr = process.argv[2];
const proxyUserPass = process.argv[3];

var timeoutSec = 30000;


const screenshotPath = './';
const index_page = 'http://fssprus.ru/'; // Главная страница фссп
const serverAdr = 'http://192.168.2.28/'
const recognizeCaptchaURL = serverAdr+'capcha';
const getContentURL = serverAdr+'search-items?limit=1';
const saveContentURL = serverAdr+'save-items';



console.log('[i] proxyAddr = ', proxyAddr);
console.log('[i] proxyUserPass = ', proxyUserPass);
console.log('[Start] ');
console.log('======================================================================== ');

// await browser.close();
if(proxyAddr && proxyUserPass){
  var params = [`--proxy=${proxyAddr} --proxy-auth=${proxyUserPass}`]
} else {
  var params = []
}
console.log('[i] Params = ', params);

var param = {}
if(proxyAddr){
  param = {
    args: [`--proxy-server=${proxyAddr}`,'--no-sandbox', '--disable-setuid-sandbox']
  }
  var username = proxyUserPass.split(':')[0]
  var password = proxyUserPass.split(':')[1]
  console.log('[i] Username is ', username);
  console.log('[i] password is ', password);
}
else {
  param = {
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  }
}
console.log('[i] Params is ', param);


(async () => {
  const browser = await puppeteer.launch(param);
  console.log('[i] Browser is connected');

  let timeout = setTimeout(async function(){ await browser.close(); return; },300000);
  const page = await browser.newPage();
  if(username) await page.authenticate({username, password});
  page.waitForNavigation({timeout: 30000})
  page.setViewport({width: 1024, height: 1768});
  await page.setRequestInterception(true);

  let requestUrl = ''

  page.on('request', request => {
    if(request.url().indexOf('ajax_search') > -1){
      console.info('Requesting', request.url());
      requestUrl = request.url();
    }
    request.continue();
  });

  await page.goto(index_page);
  console.log('[i] Page is open');
  await page.screenshot({path: screenshotPath+'test.png'});

  /**************Делаем тестовый поиск****************/
//  var data = 'АЛЕКСЕЕВА ИРИНА НИКОЛАЕВНА'
//
//  let content = await page.evaluate(function() {
//    if($('#hip-popup').length > 0){
//      $('.header-infoline-body').click();
//      return {status: 403, err: 'popup'}
//    }
//    return {status: 200, err: ''}
//  })
//  console.log("[i] Popup test return is ", content);
//
//  timeoutSec = 10000
//  console.log("[timeout] Wait "+timeoutSec+" msec before enter test data ")
//  content = await new Promise((resolve, reject) => {
//      setTimeout(async function() {
//        let content = await page.evaluate(function(data) {
//          console.log('[i] data is ',data);
//          $('#debt-form01').val(data);
//          //$('#region_id_chosen a span').val('Калининградская область');
//          $('#region_id').val(-1);
//          $('.ip_preg').submit();
//
//          return $('#debt-form01').val()
//        }, data)
//        resolve(content)
//      }, timeoutSec)
//    }
//  )
//
//  await page.screenshot({path: '/var/www/html/fssp/test1.png'});
//  console.log("[i] From index page returns ", content);
//  if(content == data){
//    console.log("[+] Resourse is ok ");
//  } else {
//    console.log("[-] Resourse is not ok ");
//    clearTimeout(timeout);
//    await browser.close()
//    return
//  }



  /**************Проверяем присутствие капчи****************/
  let timioutCheckCapcha = 20000
  console.log("[timeout] Wait "+timioutCheckCapcha+" sec Check capcha")
  let res = await new Promise((resolve, reject) => {
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
  await page.screenshot({path: '/var/www/html/fssp/test2.png'});

  console.log("[i] From next page returns ", res.status);
  if(res.status == 403){
    console.log("[err] ", res.err);
    console.log("[i] Send capcha recognize request");
    var capchaRes = '';
    capchaRes = await new Promise ((resolve, reject) => {
        let capcha = ''
        request.post({url: recognizeCaptchaURL, form: {image: res.content}}, function(err,httpResponse,body){
        if(err){
          console.log('error:', err); // Print the error if one occurred
          resolve(false)
        }
        if(httpResponse.statusCode != 200){
          console.log('statusCode:', httpResponse && httpResponse.statusCode); // Print the response status code if a response was received
        }
        try {
          console.log('body:',  body);
          resolve(JSON.parse( body ).code)
        } catch (e) {
          console.log(e);
          resolve(false)
        }
      })
    })
    console.log('[i] capchaRes is ', capchaRes);
    if(!capchaRes){
      console.log('[Fatal error] Capcha service is not responded');
      await browser.close();
      return
    }

    content = await page.evaluate(function(code) {
      $('#captcha-popup-code').val(code);
      $('#ncapcha-submit').click();

      return $('#captcha-popup-code').val();
    }, capchaRes)
    console.log('[i] From enter capcha form ',content);
    if(content == capchaRes){
      console.log("[+] Resourse on enter capcha is ok ");
    } else {
      console.log("[-] Resourse on enter capcha is not ok ");
      clearTimeout(timeout);
      await browser.close();
      return
    }
  }

  /**************Проверяем результат после ввода капчи, если его нет, то завершаем работу****************/
  timeoutSec = 20000
  console.log("[timeout] Wait "+timeoutSec+" sec ")
  res = await new Promise((resolve, reject) => {
      setTimeout(async function() {
        console.log("[i] Testing page after "+timeoutSec+" sec ")
        let r = await page.evaluate(function() {
          return $('div.results-frame').length;
        })
        console.log('[i] Is results table ', r);
        if(r > 0) resolve(true)
        else resolve(false)
      }, timeoutSec);
    }).catch((e) => {console.log(e);})
  if(!res){
    console.log("[-] Page with test result is not ok ");
    clearTimeout(timeout);
    await browser.close();
    return
  }

  /**************Берём данные для поиска****************/
  console.log("[i] Getting content ");
  let searchContent = await new Promise ((resolve, reject) => {
      request.get({url: getContentURL}, function(err,httpResponse,body){
      if(err){
        console.log('error:', err); // Print the error if one occurred
        resolve(false)
      }
      if(httpResponse.statusCode != 200){
        console.log('statusCode:', httpResponse && httpResponse.statusCode); // Print the response status code if a response was received
      }
      try {
        console.log('body:',  body);
        resolve(JSON.parse(body))
      } catch (e) {
        console.log(e);
        resolve(false)
      }
    })
  })
  console.log('[i] Geting content returns is ', searchContent);

  /**************Разбираем результат на составляющие****************/
  let tempArr = []
  tempArr = searchContent.data.split('$$')
  searchContent.f = tempArr[0]
  searchContent.i = tempArr[1]
  searchContent.o = tempArr[2]
  searchContent.dr = tempArr[3]
  console.log('[i] SearchContent modify to ',searchContent);

  /**************Выполняем боевой поиск****************/
  content = await page.evaluate(function(data) {
    console.log('[i] data is ',data);
    console.log('[i] data is ',data);
    $('#debt-form01').val(data.f+' 'data.i+' 'data.o+' 'data.dr);
    //$('#region_id_chosen a span').val('Калининградская область');
    $('#region_id').val(-1);
    $('.ip_preg').submit();
//    $('input[name="is[last_name]"]').val(data.f);
//    $('input[name="is[first_name]"]').val(data.i);
//    $('input[name="is[patronymic]"]').val(data.o);
//    $('input[name="is[date]"]').val(data.dr);
//    $('#region_id').val(-1);
//    $('#btn-sbm').click();
//    return $('div.results-frame').length
    return $('#debt-form01').val()
  }, searchContent)
  console.log('[i] div.results-frame length is', content);
  await page.screenshot({path: '/var/www/html/fssp/test3.png'});

  /**************Проверяем результат после ввода капчи, если его нет, то завершаем работу****************/
  timeoutSec = 50000
  console.log("[timeout] Wait "+timeoutSec+" sec ")
  res = await new Promise((resolve, reject) => {
      setTimeout(async function() {
        console.log("[i] Testing page after "+timeoutSec+" sec ")
        await page.screenshot({path: '/var/www/html/fssp/test4.png'});
        let r = await page.evaluate(function(dt) {
          var data = []
          var ret = {}
          if(!$('div.iss').length){
            ret.status = 500
            ret.err = 'Pege response is not contain the data block'
            return ret
          }
          if($('div.iss').html().indexOf('ничего не найдено') > -1){
            ret.status = 404
            ret.err = 'Nothing found'
            return ret
          }

          $('.iss .results table tr').each(function(kk){

              if(kk === 0 || $(this).hasClass('region-title')) {
                  // nothing
              } else {
                  var td = {};
                  $(this).find('td').each(function(k){
                      var td1 = $(this).html();
                      if(k===0){
                          td1 = td1.split('<br>');
                          if(td1.length === 3){
                              td.fio = td1[0];
                              td.birth = td1[1];
                              td.address = td1[2];
                          }
                      }
                      if(k===1){
                          td1 = td1.split('от');
                          if(td1.length === 2){
                              td.ip_no = td1[0];
                              td.ip_dt = td1[1];
                          }
                      }
                      if(k===2){
                          td1 = td1.split('<br>');
                          if(td1.length === 2){
                              td.ip_req = td1[0];
                              td.ip_req_addr = td1[1];
                          }
                          if(td1.length === 3){
                              td.ip_req = td1[0] + ' ' +  td1[1];
                              td.ip_req_addr = td1[2];
                          }
                      }
                      if(k===3){
                          td1 = td1.split('<br>');
                          if(td1.length){
                              td.ip_end_dt = td1[0];
                              td1.splice(0, 1);
                              td1 = td1.join(',');
                              td.ip_end_reason = td1;
                          }
                      }
                      if(k===4){
                          //return false;res.status
                      }
                      if(k===5){
                          td1 = td1.split('<br>');
                          if(td1.length > 0){
                              td.debt_summ_reason = td1[0];
                          }
                          if(td1.length > 1){
                              td.isp_summ_reason = td1[1];
                          }
                      }
                      if(k===6){
                          td1 = td1.split('<br>');
                          if(td1.length > 0){
                              td.fssp_name = td1[0];
                          }
                          if(td1.length > 1){
                              td.fssp_addr = td1[1];
                          }
                      }
                      if(k===7){
                          td1 = td1.split('<br>');
                          if(td1.length){
                              td.fssp_human = td1[0];
                              td1.splice(0, 1);
                              td1 = td1.join(',');
                              td.fssp_human_phones = td1;
                          }
                      }
                  });
                  td['requestUrl'] = dt.requestUrl
                  data.push(td);
              }
          });


          ret.status = 200
          ret.err = ''
          ret.data = data
          return ret
        }, {requestUrl} )
        // console.log('[i] Results of query ', r);
        resolve(r)
      }, timeoutSec);
    }).catch((e) => {console.log(e);})

  if(res.status != 200){
    console.log("[-] Page result is not ok. Response status is ", res.status);
    console.log("[Fatal error]  ", res.err);
    if(res.status == 404){
      console.log('[i] Send data for save');
      let markSearchDone = await new Promise ((resolve, reject) => {
          request.post({url: saveContentURL, form: { id: searchContent['id'], requestUrl}}, function(err,httpResponse,body){
          if(err){
            console.log('error:', err); // Print the error if one occurred
            resolve(false)
          }
          if(httpResponse.statusCode != 200){
            console.log('statusCode:', httpResponse && httpResponse.statusCode); // Print the response status code if a response was received
          }
          try {
            console.log('body:',  body);
            resolve(true)
          } catch (e) {
            console.log(e);
            resolve(false)
          }
        })
      });
      console.log('[i] Result of markSearchDone is ', markSearchDone);
    }
    clearTimeout(timeout);
    await browser.close();
    return
  }

  console.log('[+] Search result length is ', res.data.length);
  if(res.data.length < 1){
    console.log('[error] Empty result');
    clearTimeout(timeout);
    await browser.close();
    return
  }

  console.log('[+] Search result is ', res.data);
  console.log('[i] Send data for save');
  clearTimeout(timeout);
  let saveResult = await new Promise ((resolve, reject) => {
      request.post({url: saveContentURL, form: {html: encodeURIComponent(JSON.stringify(res.data)), id: searchContent['id']}}, function(err,httpResponse,body){
      if(err){
        console.log('error:', err); // Print the error if one occurred
        resolve(false)
      }
      if(httpResponse.statusCode != 200){
        console.log('statusCode:', httpResponse && httpResponse.statusCode); // Print the response status code if a response was received
      }
      try {
        console.log('body:',  body);
        resolve(true)
      } catch (e) {
        console.log(e);
        resolve(false)
      }
    })
  });

  console.log('[i] saveResult is ', saveResult)




  await browser.close();
})();

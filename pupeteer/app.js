

const puppeteer = require('puppeteer');
const request = require('request');

const proxyAddr = process.argv[2];
const proxyUserPass = process.argv[3];

var timeoutSec = 30000;

const limit_items = 2
const source_id = 39
const screenshotPath = '/var/www/skip/Api-Skip/pupeteer/screenshots/';
const index_page = 'http://fssprus.ru/'; // Главная страница фссп
// const serverAdr = 'http://192.168.110.66:8000/api/v1/'
const serverAdr = 'http://localhost:8000/api/v1/'
const recognizeCaptchaURL = serverAdr+'capcha-recognize';
const getContentURL = `${serverAdr}search-items?limit=${limit_items}&source_id=${source_id}`;
const saveContentURL = serverAdr+'search-items';


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

  let timeout = setTimeout(async function(){ await browser.close(); return; },600000);
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



  /**************Берём данные для поиска****************/
  console.log("[i] Getting content ");
  let searchPersons = await new Promise ((resolve, reject) => {
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
  console.log('[i] Geting content returns is ', searchPersons);
  searchPersons = searchPersons.payload

  await (async() => {
    if(searchPersons.length == 0){
      console.log('[end] Empty queue for search');
      clearTimeout(timeout);
      await browser.close()
      return 1
    }
  })()

  await (async () =>{
    for (i in searchPersons) {

      await page.goto(index_page);
      console.log('[i] Index page is open');
      await page.screenshot({path: screenshotPath+'start_page.png'});

      // /**************Разбираем результат на составляющие****************/
      let tempArr = []
      tempArr = searchPersons[i].search_str.split('|')
      searchContent = {}
      searchContent.f = tempArr[0]
      searchContent.i = tempArr[1]
      searchContent.o = tempArr[2]
      searchContent.dr = tempArr[3]
      searchContent.id = searchPersons[i]['id']
      console.log('[i] SearchContent modify to ',searchContent);


      /**************Выполняем боевой поиск****************/
      content = await page.evaluate(function(data) {
        console.log('[i] data is ',data);
        console.log('[i] data is ',data);
        $('#debt-form01').val(data.f+' '+data.i+' '+data.o+' '+data.dr);
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
      await page.screenshot({path: screenshotPath+'start_page_with_data.png'});

      if(content == searchContent.f+' '+searchContent.i+' '+searchContent.o+' '+searchContent.dr){
        console.log("[+] Resourse is ok ");
      } else {
        console.log("[-] Resourse is not ok ");
        clearTimeout(timeout);
        await browser.close()
        break
        return
      }

      /**************Проверяем присутствие капчи****************/
      let timioutCheckCapcha = 25000
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
      await page.screenshot({path: screenshotPath+'test_capcha.png'});

      /**************Если она есть****************/
      if(res.status == 403){
        console.log("[err] ", res.err);
        console.log("[i] Send capcha recognize request by URL ", recognizeCaptchaURL);
        var capchaRes = '';
        capchaRes = await new Promise ((resolve, reject) => {
            let capcha = ''
            request.post({url: recognizeCaptchaURL, form: {capcha_img: res.content}}, function(err,httpResponse,body){
            if(err){
              console.log('error:', err); // Print the error if one occurred
              resolve(false)
            }
            if(httpResponse.statusCode != 200){
              console.log('statusCode:', httpResponse && httpResponse.statusCode); // Print the response status code if a response was received
            }
            try {
              console.log('body:',  body);
              let ret = {}
              ret.result = JSON.parse( body ).payload
              ret.status = httpResponse.statusCode
              resolve(ret)
            } catch (e) {
              console.log(e);
              resolve(false)
              browser.close();
              clearTimeout(timeout);
              return
            }
          })
        })
        console.log('[i] capchaRes is ', capchaRes);
        if(!capchaRes){
          console.log('[Fatal error] Capcha service is not responded');
          await browser.close();
          clearTimeout(timeout);
          return
        }
        if(capchaRes.status == 404){
          console.log('[Error] Capcha not recognized');
          continue
        }

        content = await page.evaluate(function(code) {
          $('#captcha-popup-code').val(code);
          $('#ncapcha-submit').click();

          return $('#captcha-popup-code').val();
        }, capchaRes.result)
        console.log('[i] From enter capcha form ',content);
        if(content == capchaRes.result){
          console.log("[+] Resourse on enter capcha is ok ");
        } else {
          console.log("[-] Resourse on enter capcha is not ok ");
          clearTimeout(timeout);
          await browser.close();
          break
          return
        }
      }


      /**************Проверяем результат после ввода капчи, если его нет, то завершаем работу****************/
      timeoutSec = 120000
      console.log("[timeout] Wait "+timeoutSec+" sec ")
      res = await new Promise((resolve, reject) => {
        setTimeout(async function() {
          console.log("[i] Testing page after "+timeoutSec+" sec ")
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

            console.log('[Check] iss .results table tr length',$('.iss .results table tr').length);

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
            ret.table_length = $('.iss .results table tr').length
            return ret
          }, {requestUrl} )
            // console.log('[i] Results of query ', r);
            resolve(r)
        }, timeoutSec);
      }).catch((e) => {console.log(e);})
      await page.screenshot({path: screenshotPath+'result_after_enter_capcha.png'});

      console.log("[i] Res after set capcha is ", res)

      if(res.status != 200){
        if(res.status == 404){
          console.log('[i] Send data for save');
          let markSearchDone = await new Promise ((resolve, reject) => {
              request.post({url: saveContentURL, json: { id: searchContent['id'], requestUrl}}, function(err,httpResponse,body){
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
        continue;
      }

      if(res.data.length == 0) {
        console.log('[Fatal error] Response data is empty');
        continue;
      }


      console.log('[i] Send data for save');
      // clearTimeout(timeout);
      if(res.data[0]){
        let saveResult = await new Promise ((resolve, reject) => {
            request.post({url: saveContentURL, json: {data: res.data, id: searchContent['id'], requestUrl}}, function(err,httpResponse,body){
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
      }
      console.log("[i] End iteration")

    }
  })()

  clearTimeout(timeout);
  await browser.close();



//



  await browser.close();
}) ().catch(e => console.log(e));

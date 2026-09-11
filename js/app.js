/* Classic deferred scripts support both file:// and GitHub Pages without fetch/build. */
(() => {
  "use strict";
  const data=window.UNIVERSE_DATA;
  const $=id=>document.getElementById(id);
  const reducedMotion=window.matchMedia("(prefers-reduced-motion: reduce)");
  const app={data,state:{quizComplete:false,openedLetters:[]}};
  app.element=(tag,text,attributes={})=>{const node=document.createElement(tag);if(text!==null&&text!==undefined)node.textContent=text;Object.entries(attributes).forEach(([key,value])=>node.setAttribute(key,String(value)));return node;};
  app.image=(src,alt,className="")=>{
    const img=app.element("img",null,{src,alt,class:className,loading:"lazy",decoding:"async",width:720,height:800});
    img.addEventListener("error",()=>{img.src="assets/images/photo-placeholder.svg";},{once:true});return img;
  };
  function paragraphs(target,items){items.forEach(text=>target.append(app.element("p",text)));}
  function dateLabel(value){try{return new Intl.DateTimeFormat("vi-VN",{day:"2-digit",month:"2-digit",year:"numeric",timeZone:data.timeZone}).format(new Date(value.length===10?`${value}T12:00:00+07:00`:value));}catch{return "Ngày đang được viết tiếp";}}
  try{const saved=JSON.parse(localStorage.getItem(data.storageKey));if(saved&&typeof saved==="object"){app.state.quizComplete=saved.quizComplete===true;app.state.openedLetters=Array.isArray(saved.openedLetters)?saved.openedLetters.filter(id=>typeof id==="string"&&data.letters.some(letter=>letter.id===id)):[];}}catch{/* Keep the experience usable when storage is blocked or corrupt. */}
  app.save=()=>{try{localStorage.setItem(data.storageKey,JSON.stringify(app.state));}catch{/* State remains in memory for this visit. */}};
  document.title=data.siteName;$("hero-title").replaceChildren();
  const titleParts=data.siteName==="Our Little Universe"?["Our Little","Universe"]:[data.siteName,""];
  $("hero-title").append(document.createTextNode(titleParts[0]),app.element("br"),app.element("em",titleParts[1]),app.element("span","✧",{class:"title-star","aria-hidden":"true"}));
  $("intro").textContent=data.intro;
  $("couple").append(document.createTextNode(data.names[0]),app.element("span","&"),document.createTextNode(data.names[1]));
  $("hero-image").src=data.heroImage;$("hero-image").alt=data.heroAlt;$("hero-caption").textContent=data.heroCaption;
  $("hero-image").addEventListener("error",()=>{$("hero-image").src="assets/images/photo-placeholder.svg";},{once:true});
  $("map-image").src=data.mapImage;
  paragraphs($("reason-copy"),data.reason);$("signature").textContent=data.signature;
  $("footer-names").textContent=`${data.names.join(" & ")} · ${data.siteName}`;
  $("start-date").textContent=`Kể từ ngày ${dateLabel(data.startDate)}`;
  app.dialog=$("memory-dialog");app.dialogContent=$("dialog-content");let opener=null;
  app.openDialog=(source,render,gallery=false)=>{
    opener=source;app.dialogContent.replaceChildren();$("lightbox-controls").hidden=!gallery;render();
    app.dialog.showModal();document.body.classList.add("modal-open");app.dialog.querySelector(".dialog-close").focus();
  };
  app.dialog.querySelector(".dialog-close").addEventListener("click",()=>app.dialog.close());
  app.dialog.addEventListener("click",event=>{const r=app.dialog.getBoundingClientRect();if(event.target===app.dialog&&(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom))app.dialog.close();});
  app.dialog.addEventListener("close",()=>{document.body.classList.remove("modal-open");if(opener?.isConnected)opener.focus({preventScroll:true});});
  // Keep Tab inside the dialog, including at the browser chrome boundary.
  app.dialog.addEventListener("keydown",event=>{
    if(event.key!=="Tab")return;
    const focusable=[...app.dialog.querySelectorAll('button:not(:disabled),a[href],[tabindex="0"]')].filter(node=>node.getClientRects().length);
    const first=focusable[0],last=focusable[focusable.length-1];
    if(event.shiftKey&&document.activeElement===first){event.preventDefault();last.focus();}
    else if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first.focus();}
  });
  data.timeline.forEach(item=>{
    const article=app.element("article",null,{class:"timeline-item reveal"});
    const copy=app.element("div",null,{class:"timeline-copy"});copy.append(app.element("time",dateLabel(item.date),{datetime:item.date}),app.element("h3",item.title),app.element("p",item.text),app.element("small",item.label));
    article.append(app.image(item.image,item.alt,"timeline-image"),app.element("span",item.icon,{class:"timeline-symbol","aria-hidden":"true"}),copy);$("timeline").append(article);
  });
  data.places.forEach((place,index)=>{
    const pin=app.element("button",index+1,{type:"button",class:"map-pin","aria-label":`Mở kỷ niệm: ${place.name}`});
    pin.style.left=`${Math.max(8,Math.min(92,place.x))}%`;pin.style.top=`${Math.max(8,Math.min(92,place.y))}%`;
    const legend=app.element("button",null,{type:"button"});legend.append(app.element("span",`${index+1}.`),document.createTextNode(place.name));
    [pin,legend].forEach(button=>button.addEventListener("click",()=>app.openDialog(button,()=>{app.dialogContent.append(app.image(place.image,place.alt,"dialog-image"),app.element("h2",place.name,{id:"dialog-title"}),app.element("time",dateLabel(place.date),{datetime:place.date}),app.element("p",place.story));})));
    $("memory-map").append(pin);$("map-legend").append(legend);
  });
  data.love.forEach((item,index)=>{const card=app.element("article",null,{class:"love-card reveal"});card.append(app.element("span",String(index+1).padStart(2,"0")),app.element("h3",item.title),app.element("p",item.text));$("love-cards").append(card);});
  data.letters.forEach(letter=>{
    const button=app.element("button",null,{type:"button",class:"envelope"});
    const status=app.element("small",app.state.openedLetters.includes(letter.id)?"Đã mở · Đọc lại ↗":"Chạm để mở");
    button.append(app.element("span",null,{class:"envelope-flap","aria-hidden":"true"}),app.element("span","♡",{class:"wax","aria-hidden":"true"}),app.element("span",letter.title,{class:"envelope-label"}),status);
    if(app.state.openedLetters.includes(letter.id))button.classList.add("opened");
    button.addEventListener("click",()=>{
      if(!app.state.openedLetters.includes(letter.id)){app.state.openedLetters.push(letter.id);app.save();}button.classList.add("opened");status.textContent="Đã mở · Đọc lại ↗";
      app.openDialog(button,()=>{app.dialogContent.append(app.element("p","MỘT CÁI ÔM BẰNG NHỮNG DÒNG CHỮ",{class:"eyebrow"}),app.element("h2",letter.title,{id:"dialog-title"}));const content=app.element("div",null,{class:"prose"});paragraphs(content,letter.text);if(letter.quote)content.append(app.element("blockquote",letter.quote));app.dialogContent.append(content);});
    });$("letters-grid").append(button);
  });
  let finalOpened=false;
  $("final-envelope").addEventListener("click",()=>{
    if(finalOpened){$("final-letter").focus({preventScroll:true});return;}finalOpened=true;
    $("final-envelope").classList.add("opened");$("final-envelope").setAttribute("aria-expanded","true");$("final-envelope").querySelector("small").textContent="Đã mở · Lá thư ở ngay bên dưới";
    const show=()=>{
      const letter=$("final-letter");letter.append(app.element("h3",data.finalLetter.title));paragraphs(letter,data.finalLetter.paragraphs);letter.append(app.element("p",data.finalLetter.signature,{class:"signature"}));letter.hidden=false;letter.focus({preventScroll:true});letter.scrollIntoView({behavior:reducedMotion.matches?"instant":"smooth",block:"start"});
      if(!reducedMotion.matches){for(let i=0;i<18;i++){const confetti=app.element("span",null,{class:"confetti","aria-hidden":"true"});confetti.style.setProperty("--x",`${15+Math.random()*70}%`);confetti.style.setProperty("--c",["#b87a78","#adb59b","#c6a573"][i%3]);document.body.append(confetti);setTimeout(()=>confetti.remove(),2200);}}
    };if(reducedMotion.matches)show();else setTimeout(show,400);
  });
  $("countdown-caption").textContent=data.countdownCaption;
  const units=[["days","ngày"],["hours","giờ"],["minutes","phút"],["seconds","giây"]];
  units.forEach(([key,label])=>{const unit=app.element("div",null,{class:"countdown-unit"});unit.append(app.element("strong","00",{id:`count-${key}`}),app.element("span",label));$("countdown").append(unit);});
  let giftShown=false;
  app.updateGift=()=>{
    const remaining=UniverseClock.remaining(data.targetDate),timeReady=data.bypassCountdown||remaining.ended;
    const ready=app.state.quizComplete&&timeReady;
    $("gift-open").disabled=!ready;
    const missing=[];if(!app.state.quizComplete)missing.push("hoàn thành trò chơi để nhận chìa khóa");if(!timeReady)missing.push(remaining.valid?"chờ đến ngày hẹn":"kiểm tra lại ngày hẹn trong cấu hình");
    const giftStatus=ready?"Đã có chìa khóa, ngày hẹn cũng đã đến. Bất ngờ này dành cho em!":`Mình chỉ còn ${missing.join(" và ")} nhé.`;
    if($("gift-status").textContent!==giftStatus)$("gift-status").textContent=giftStatus;
    if(!ready&&giftShown){$("gift-content").hidden=true;$("gift-open").hidden=false;giftShown=false;}
  };
  function tick(){
    const start=UniverseClock.timestamp(data.startDate),elapsed=UniverseClock.elapsed(data.startDate),remaining=UniverseClock.remaining(data.targetDate);
    $("days-together").textContent=elapsed.days.toLocaleString("vi-VN");
    $("together-detail").textContent=!Number.isFinite(start)?"Hãy kiểm tra ngày bắt đầu trong cấu hình.":Date.now()<start?"Câu chuyện của chúng mình sắp bắt đầu.":`${elapsed.hours} giờ · ${elapsed.minutes} phút · ${elapsed.seconds} giây, và vẫn đang đếm…`;
    units.forEach(([key])=>{$(`count-${key}`).textContent=String(data.bypassCountdown?0:remaining[key]).padStart(2,"0");});
    const status=!remaining.valid?"Ngày hẹn chưa hợp lệ. Hãy dùng ngày ISO có múi giờ.":data.bypassCountdown?"Đang thử nghiệm: đã bỏ qua thời gian chờ.":remaining.ended?"Ngày đặc biệt đã đến. Mình cùng tạo thêm kỷ niệm nhé!":"Mỗi giây trôi qua, mình lại gần cuộc hẹn hơn một chút.";
    if($("countdown-status").textContent!==status)$("countdown-status").textContent=status;
    app.updateGift();
  }
  $("gift-open").addEventListener("click",()=>{
    const timeReady=data.bypassCountdown||UniverseClock.remaining(data.targetDate).ended;
    if(!app.state.quizComplete||!timeReady)return;
    const content=$("gift-content");content.replaceChildren(app.image(data.gift.image,data.gift.alt),app.element("h3",data.gift.title,{tabindex:"-1"}),app.element("p",data.gift.text),app.element("p",data.gift.invitation));content.hidden=false;$("gift-open").hidden=true;giftShown=true;content.querySelector("h3").focus({preventScroll:true});
  });
  UniverseGallery.init(app);UniverseQuiz.init(app);tick();setInterval(tick,1000);
  document.addEventListener("visibilitychange",()=>{if(!document.hidden)tick();});
  window.addEventListener("storage",event=>{if(event.key===data.storageKey&&event.newValue){try{const state=JSON.parse(event.newValue);if(state.quizComplete===true){app.state.quizComplete=true;app.updateGift();}}catch{/* Ignore malformed values. */}}});
  const music=$("music");
  if(data.audioSrc){
    const audio=new Audio();audio.preload="none";audio.loop=true;audio.volume=.35;audio.src=data.audioSrc;
    music.disabled=false;music.querySelector("span").textContent="Bật nhạc";
    const update=playing=>{music.setAttribute("aria-pressed",String(playing));music.querySelector("span").textContent=playing?"Tắt nhạc":"Bật nhạc";};
    audio.addEventListener("error",()=>{update(false);music.disabled=true;music.querySelector("span").textContent="Nhạc chưa khả dụng";$("music-status").textContent="Không tải được nhạc. Em vẫn có thể tiếp tục khám phá.";});
    audio.addEventListener("pause",()=>update(false));audio.addEventListener("play",()=>update(true));
    music.addEventListener("click",async()=>{if(audio.paused){try{await audio.play();}catch{update(false);$("music-status").textContent="Chưa phát được nhạc. Hãy thử lại hoặc kiểm tra tệp âm thanh.";}}else audio.pause();});
  }else music.title="Thêm đường dẫn audioSrc trong js/data.js để bật nhạc nền.";
  $("start").addEventListener("click",()=>{$("together").setAttribute("tabindex","-1");$("together").focus({preventScroll:true});});
  if("IntersectionObserver" in window&&!reducedMotion.matches){
    const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.remove("waiting");observer.unobserve(entry.target);}}),{threshold:.08});
    document.querySelectorAll(".reveal").forEach(node=>{node.classList.add("waiting");observer.observe(node);});
  }
})();

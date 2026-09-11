window.UniverseQuiz = {
  init(app) {
    const card=document.getElementById("quiz-card"),questions=app.data.quiz;
    let index=0,score=0;
    function result(focus=false){
      card.replaceChildren(app.element("p","✧ CHÌA KHÓA KỶ NIỆM",{class:"eyebrow"}));
      const title=app.element("h3","Chúng mình nhớ thật nhiều!",{tabindex:"-1"});
      card.append(title,app.element("p",focus?`Em đã nhớ đúng ${score}/${questions.length} câu. Nhưng kỷ niệm nào cũng đáng giữ, dù mình nhớ khác nhau một chút. Chiếc chìa khóa là của em!`:"Em đã nhận được chiếc chìa khóa kỷ niệm. Món quà sẽ sẵn sàng khi ngày đặc biệt đến.",{class:"quiz-result"}));
      const replay=app.element("button","Chơi lại ↻",{type:"button",class:"button primary"});
      replay.addEventListener("click",()=>{index=0;score=0;render(true);});
      card.append(replay);if(focus)title.focus({preventScroll:true});
    }
    function render(focus=false){
      const q=questions[index];
      card.replaceChildren();
      const meta=app.element("div",null,{class:"quiz-meta"});meta.append(app.element("span",`CÂU ${index+1} / ${questions.length}`),app.element("span","Ký ức của hai đứa"));
      const title=app.element("h3",q.question,{tabindex:"-1"});
      const options=app.element("div",null,{class:"quiz-options","aria-label":"Chọn một đáp án"});
      const feedback=app.element("p","",{class:"quiz-feedback",role:"status"});
      const next=app.element("button",index===questions.length-1?"Nhận chìa khóa ✧":"Câu tiếp theo →",{type:"button",class:"button primary quiz-next"});next.hidden=true;
      let answered=false;
      q.options.forEach((option,i)=>{
        const button=app.element("button",`${String.fromCharCode(65+i)}. ${option}`,{type:"button",class:"quiz-option"});
        button.addEventListener("click",()=>{
          if(answered)return;answered=true;
          const correct=i===q.correct;if(correct)score++;
          [...options.children].forEach(child=>child.disabled=true);
          button.classList.add("selected");button.textContent=`${correct?"✓":"♡"} ${option}`;
          if(options.children[q.correct])options.children[q.correct].classList.add("correct");
          feedback.textContent=correct?q.yes:q.no;next.hidden=false;next.focus({preventScroll:true});
        });options.append(button);
      });
      next.addEventListener("click",()=>{
        if(!answered)return;
        if(index===questions.length-1){app.state.quizComplete=true;app.save();app.updateGift();result(true);}
        else{index++;render(true);}
      });
      card.append(meta,app.element("progress",null,{max:questions.length,value:index,"aria-label":"Tiến trình quiz"}),title,options,feedback,next);
      if(focus)title.focus({preventScroll:true});
    }
    if(!questions.length){card.append(app.element("p","Chưa có câu hỏi. Hãy thêm câu hỏi trong js/data.js."));return;}
    if(app.state.quizComplete)result();else render();
  }
};

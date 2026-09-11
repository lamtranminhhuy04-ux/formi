window.UniverseGallery = {
  init(app) {
    const photos=app.data.photos;
    let current=0;
    const controls=document.getElementById("lightbox-controls");
    function display() {
      const photo=photos[current];
      app.dialogContent.replaceChildren(app.image(photo.image,photo.alt,"dialog-image"),app.element("h2",photo.caption,{id:"dialog-title"}));
      document.getElementById("photo-position").textContent=`${current+1} / ${photos.length}`;
    }
    function change(step){if(!photos.length)return;current=(current+step+photos.length)%photos.length;display();}
    photos.forEach((photo,index)=>{
      const button=app.element("button",null,{type:"button",class:"polaroid","aria-label":`Xem ảnh: ${photo.caption}`});
      button.style.setProperty("--tilt",`${[-3,2,-2,3,-2,2][index%6]}deg`);
      button.append(app.element("span",null,{class:"tape","aria-hidden":"true"}),app.image(photo.image,photo.alt),app.element("span",photo.caption,{class:"caption"}));
      button.addEventListener("click",()=>{current=index;app.openDialog(button,display,true);});
      document.getElementById("gallery").append(button);
    });
    document.getElementById("photo-prev").addEventListener("click",()=>change(-1));
    document.getElementById("photo-next").addEventListener("click",()=>change(1));
    app.dialog.addEventListener("keydown",event=>{
      if(controls.hidden)return;
      if(event.key==="ArrowLeft"||event.key==="ArrowRight"){event.preventDefault();change(event.key==="ArrowLeft"?-1:1);}
    });
    if(!photos.length)document.getElementById("gallery").append(app.element("p","Những tấm ảnh mới đang chờ được thêm vào.",{class:"empty-state"}));
  }
};

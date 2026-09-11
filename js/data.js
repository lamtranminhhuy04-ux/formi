/* TOÀN BỘ NỘI DUNG BÊN DƯỚI LÀ MẪU. Thay chuỗi trong dấu ngoặc kép.
   Dùng đường dẫn tương đối: assets/images/ten-anh.webp. Không thêm dấu / đầu đường dẫn.
   Ngày giờ ISO phải có múi giờ: +07:00 là Việt Nam. */
window.UNIVERSE_DATA = {
  siteName: "Our Little Universe",
  names: ["Mây", "Nắng"],
  startDate: "2024-02-14T00:00:00+07:00",
  targetDate: "2027-02-14T19:00:00+07:00",
  timeZone: "Asia/Ho_Chi_Minh",
  intro: "Giữa thế giới rộng lớn này, thật may vì chúng mình đã tìm thấy nhau.",
  heroImage: "assets/images/hero-placeholder.svg",
  heroAlt: "Minh họa hai người ngồi bên nhau ngắm biển lúc hoàng hôn",
  heroCaption: "Chúng mình, và những ngày thật dịu dàng.",
  reason: ["Anh tạo nên nơi này để cất những điều đôi khi chúng mình vô tình bỏ quên: một buổi chiều cùng đi dạo, một câu nói làm cả hai bật cười, hay một ngày bình thường mà có em ở cạnh.", "Để một ngày nào đó, khi cuộc sống hơi vội, chúng mình có thể ghé lại đây. Lật từng trang, nhớ từng chút, và thấy rằng: mình đã có với nhau thật nhiều điều đẹp đẽ."],
  signature: "Thương em, Mây.",
  mapImage: "assets/images/map-placeholder.svg",
  // x, y là phần trăm trong ảnh bản đồ, nên đặt trong khoảng 8–92.
  places: [
    {name:"Góc cà phê quen",date:"2024-01-28",x:23,y:34,image:"assets/images/cafe.svg",alt:"Hai tách cà phê trên bàn bên cửa sổ",story:"Hai ly nước đã nguội từ lâu, còn câu chuyện của chúng mình thì mãi chưa hết."},
    {name:"Đà Lạt mộng mơ",date:"2024-06-15",x:64,y:25,image:"assets/images/mountains.svg",alt:"Những ngọn đồi xanh và ngôi nhà giữa rừng thông",story:"Sáng sớm hơi lạnh, một chiếc áo khoác chia đôi và con đường không cần biết trước điểm đến."},
    {name:"Biển chiều hôm ấy",date:"2025-04-30",x:77,y:69,image:"assets/images/hero-placeholder.svg",alt:"Hai người bên biển lúc mặt trời lặn",story:"Em bảo hoàng hôn hôm nay đẹp quá. Anh nghĩ, có lẽ vì người ngồi bên cạnh."},
    {name:"Công viên nhỏ",date:"2025-09-02",x:35,y:73,image:"assets/images/picnic.svg",alt:"Giỏ picnic và hoa trên tấm khăn giữa bãi cỏ",story:"Một buổi picnic chẳng có kế hoạch. Bánh hơi cháy, nhưng tiếng cười thì vừa đủ ngọt."}
  ],
  timeline: [
    {date:"2024-01-12",title:"Ngày hai đường thẳng giao nhau",text:"Một lời chào rất bình thường. Ai ngờ lại là bắt đầu của biết bao điều đặc biệt.",icon:"✦",image:"assets/images/cafe.svg",alt:"Góc quán cà phê ấm áp",label:"Lần đầu gặp nhau"},
    {date:"2024-01-28",title:"Một buổi hẹn, nhiều bối rối",text:"Anh đến sớm mười lăm phút. Em cười một cái, mọi câu đã chuẩn bị đều quên mất.",icon:"☕",image:"assets/images/flowers.svg",alt:"Bó hoa nhỏ gói bằng giấy màu kem",label:"Buổi hẹn đầu tiên"},
    {date:"2024-02-14",title:"Từ hôm nay, là chúng mình",text:"Không cần một lời thật lớn. Chỉ một cái gật đầu, và một bàn tay được nắm lấy.",icon:"♡",image:"assets/images/hero-placeholder.svg",alt:"Hai người ngồi cạnh nhau bên bờ biển",label:"Ngày chính thức yêu"},
    {date:"2024-06-15",title:"Đi trốn cùng nhau",text:"Lạc đường một chút, chụp thật nhiều ảnh. Chuyến đi đẹp nhất là chuyến đi có em.",icon:"⌁",image:"assets/images/mountains.svg",alt:"Con đường uốn quanh những ngọn đồi",label:"Chuyến đi đáng nhớ"},
    {date:"2025-09-02",title:"Chiếc bánh không hoàn hảo",text:"Bánh hơi cháy, bếp hơi bừa. Nhưng hôm ấy chúng mình đã cười đến đau cả bụng.",icon:"✳",image:"assets/images/picnic.svg",alt:"Bánh và trái cây trên tấm khăn picnic",label:"Một kỷ niệm vui"},
    {date:"2026-09-11",title:"Vẫn muốn chọn em, mỗi ngày",text:"Còn nhiều nơi chưa đến, nhiều chuyện chưa kể. Mình cứ chậm rãi viết tiếp, nhé.",icon:"∞",image:"assets/images/night.svg",alt:"Hai chiếc ghế dưới bầu trời đầy sao",label:"Hiện tại và tương lai"}
  ],
  photos: [
    {image:"assets/images/hero-placeholder.svg",alt:"Hai người nhìn ra biển lúc hoàng hôn",caption:"Hôm ấy, trời cũng dịu dàng ♡"},
    {image:"assets/images/cafe.svg",alt:"Hai ly cà phê cạnh cửa sổ",caption:"Một góc quen. Một người thương."},
    {image:"assets/images/mountains.svg",alt:"Nhà nhỏ giữa những đồi thông",caption:"Lạc đường, nhưng có nhau."},
    {image:"assets/images/flowers.svg",alt:"Bó hoa hồng đất và cúc trắng",caption:"Chẳng cần một dịp đặc biệt."},
    {image:"assets/images/picnic.svg",alt:"Giỏ picnic trên bãi cỏ xanh",caption:"Ngày bình thường yêu thích nhất."},
    {image:"assets/images/night.svg",alt:"Ghế đôi dưới trăng và sao",caption:"Còn cả bầu trời để cùng ngắm."}
  ],
  love: [
    {title:"Nụ cười của em",text:"Cách mắt em cong lại mỗi khi cười. Một điều bé xíu, mà làm sáng cả ngày của anh."},
    {title:"Những thói quen nhỏ",text:"Em luôn để dành miếng ngon cuối cùng. Rồi giả vờ bảo là mình đã no."},
    {title:"Cách em lắng nghe",text:"Không cần giải quyết mọi chuyện. Em chỉ ngồi đó, và anh thấy lòng nhẹ đi."},
    {title:"Sự dịu dàng ấy",text:"Cảm ơn em vì đã ở lại cả những ngày anh không phải phiên bản tốt nhất."},
    {title:"Những ngày phía trước",text:"Anh muốn cùng em đi chợ, trồng một cái cây, và già đi qua những ngày bình thường."}
  ],
  // correct: chỉ số đáp án đúng, bắt đầu từ 0. Đổi cả phản hồi khi đổi đáp án.
  quiz: [
    {question:"Buổi hẹn đầu tiên của mình ở đâu nhỉ?",options:["Một góc cà phê","Rạp chiếu phim","Bên bờ biển"],correct:0,yes:"Đúng rồi! Góc cửa sổ ấy vẫn là chỗ anh thích nhất.",no:"Là góc cà phê nhỏ ấy. Không sao, mình lại hẹn ở đó nhé!"},
    {question:"Ai đã đến sớm trong buổi hẹn đầu?",options:["Em","Anh","Cả hai đến cùng lúc"],correct:1,yes:"Anh đó! Hồi hộp nên không thể ở nhà thêm được nữa.",no:"Hôm ấy anh đến sớm. Chắc tại mong gặp em quá thôi."},
    {question:"Chuyến đi xa đầu tiên là đến…",options:["Hội An","Đà Lạt","Hà Nội"],correct:1,yes:"Đà Lạt, và chiếc áo khoác chia đôi ♡",no:"Là Đà Lạt! Còn những nơi kia mình sẽ cùng đến."},
    {question:"Chiếc bánh tự làm hôm ấy thế nào?",options:["Hoàn hảo luôn","Hơi cháy một chút","Chưa kịp nướng"],correct:1,yes:"Hơi cháy, nhưng kỷ niệm thì ngọt vừa đủ!",no:"Hơi cháy một chút thôi. Anh vẫn cho ngày hôm ấy mười điểm."},
    {question:"Điều anh muốn làm tiếp theo là gì?",options:["Cùng em có thêm kỷ niệm","Đi hết mọi nơi một mình","Bỏ quên cuốn scrapbook"],correct:0,yes:"Đúng rồi. Mọi kế hoạch đẹp nhất đều có em.",no:"Là cùng em có thêm kỷ niệm. Câu này anh sẽ nhắc em mỗi ngày ♡"}
  ],
  letters: [
    {id:"sad",title:"Mở khi em buồn",text:["Em không cần phải ổn ngay hôm nay. Cứ cho mình một chút thời gian, uống một cốc nước ấm và hít thở thật chậm.","Anh ở đây. Em có thể kể mọi chuyện, hoặc chẳng nói gì cả. Mình ngồi cạnh nhau cũng được."],quote:"Một ngày không vui không làm em bớt đáng yêu."},
    {id:"miss",title:"Mở khi em nhớ anh",text:["Anh đoán lúc này em đang ước anh ở gần hơn một chút. Anh cũng vậy.","Cho đến lần gặp tới, hãy coi lá thư này là một cái ôm được gấp thật nhỏ. Và nhớ kể anh nghe hôm nay của em nhé."],quote:"Khoảng cách chỉ là quãng đường, không phải khoảng lòng."},
    {id:"confidence",title:"Mở khi em thiếu tự tin",text:["Có thể hôm nay em chưa nhìn thấy những điều tốt đẹp ở mình. Nhưng anh vẫn thấy: sự tử tế, lòng kiên nhẫn và cách em luôn cố gắng.","Em không cần trở thành một ai khác để xứng đáng được yêu thương. Cứ đi từng bước nhỏ, anh cổ vũ em."],quote:"Em đã đi xa hơn em nghĩ nhiều rồi."},
    {id:"angry",title:"Mở khi chúng ta giận nhau",text:["Mình có thể tạm nghỉ một chút để bình tĩnh lại. Anh muốn hiểu em, và cũng muốn được em lắng nghe.","Khi cả hai sẵn sàng, mình nói lại từ đầu nhé. Chúng mình cùng tìm cách giải quyết, bằng sự tôn trọng dành cho nhau."],quote:"Mình vẫn là một đội, kể cả trong những ngày khó."}
  ],
  finalLetter: {title:"Em thương,",paragraphs:["Nếu em đã đi đến tận đây, chắc em cũng vừa cùng anh sống lại một đoạn đường rất đẹp. Từ lời chào đầu tiên đến những ngày chúng mình chẳng làm gì đặc biệt ngoài việc ở bên nhau.","Anh không nhớ hết mọi ngày đã trôi qua. Nhưng anh nhớ cảm giác khi có em: được là chính mình, được kể những chuyện rất nhỏ, được có một người để nghĩ đến khi nhìn thấy điều gì đẹp.","Anh không hứa rằng ngày nào cũng dễ dàng. Có lúc mình sẽ mệt, sẽ bất đồng, sẽ cần học cách lắng nghe nhau thêm một chút. Anh muốn cùng em học những điều ấy, bằng sự chân thành và kiên nhẫn.","Mong những trang tiếp theo vẫn có những chuyến đi, những bữa cơm giản dị, một vài tấm ảnh hơi nhòe, và rất nhiều tiếng cười. Mình không cần vội. Chỉ cần tiếp tục dành chỗ cho nhau.","Cảm ơn em đã bước vào vũ trụ nhỏ này. Và cảm ơn em, vì đã cùng anh biến những điều bình thường thành kỷ niệm."],signature:"Thương em, hôm nay và những ngày sau.\nMây"},
  countdownCaption: "Một cuộc hẹn dành cho hai người, vào ngày 14 tháng 2 năm 2027.",
  gift: {title:"Một buổi hẹn không cần vội",text:"Để dành cho anh một buổi chiều nhé. Mình sẽ ghé quán quen, đi dạo một vòng, rồi cùng viết thêm một trang vào cuốn scrapbook này.",image:"assets/images/flowers.svg",alt:"Bó hoa nhỏ dành cho buổi hẹn",invitation:"Lời mời mẫu · 19:00, ngày 14/02/2027 · Góc cà phê quen"},
  audioSrc: "", // Đặt nhạc có quyền sử dụng vào assets/audio rồi điền đường dẫn; để trống để vô hiệu hóa.
  bypassCountdown: false, // CHỈ KIỂM THỬ. Không bảo mật; vẫn cần hoàn thành quiz.
  storageKey: "our-little-universe-v1" // Đổi hậu tố để bắt đầu lại trạng thái cho một phiên bản mới.
};

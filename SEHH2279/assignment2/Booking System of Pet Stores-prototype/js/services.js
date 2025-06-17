function selectTypeOnClick(ref) {
    var findOldButton = document.getElementsByName("selectedType")[0];
    findOldButton.removeAttribute("name");
    findOldButton.classList.remove("selected");
    ref.name = "selectedType";
    ref.classList.add("selected");
    document.getElementsByName("typeBlock").forEach((element) => {
        element.style.display = "none";
    });
    switch(ref.id) {
        case "all":
            document.getElementById("blockForHomeStay").style.display = "";
            document.getElementById("blockForBeauty").style.display = "";
            document.getElementById("blockForFood").style.display = "";
            document.getElementById("blockForSporty").style.display = "";
            break;
        case "homestay":
            document.getElementById("blockForHomeStay").style.display = "";
            break;
        case "beauty":
            document.getElementById("blockForBeauty").style.display = "";
            break;
        case "food":
            document.getElementById("blockForFood").style.display = "";
            break;
        case "sporty":
            document.getElementById("blockForSporty").style.display = "";
            break;

    }
  }
  
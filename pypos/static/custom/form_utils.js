const file_input = document.querySelector("#file_input")
file_input.addEventListener("onchange", (event) => {
    if (event.target.files.length > 0) {
        var src = URL.createObjectURL(event.target.files[0]);
        var preview = document.getElementById("image_preview");
        preview.src = src;
        preview.style.display = "block";
    }
})
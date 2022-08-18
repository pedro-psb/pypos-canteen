const file_input = document.querySelector("#file_input")
file_input.addEventListener("change", (event) => {
    console.log(event.target.files)
    if (event.target.files.length > 0) {
        var src = URL.createObjectURL(event.target.files[0]);
        var preview = document.getElementById("img_preview");
        preview.src = src;
        preview.style.display = "block";
    }
})
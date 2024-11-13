function HideDocs() {
    const meatSelector = document.getElementById("id_dispatch_note-meat_type")
    const hideBody = document.getElementById("cow-docs")
    const passports = document.getElementById("id_dispatch_note-passports")

    if(meatSelector.options[meatSelector.selectedIndex].value == "1")
    {
        hideBody.classList.remove("d-none");
        if(passports.value.length < 1)
        {
            passports.value="RS\n";
        }
    }
    else
    {
        hideBody.classList.add("d-none");
    }
};
function CalcMass() {
    const quantity = document.getElementById("id_dispatch_note-quantity")
    const tMass = document.getElementById("id_dispatch_note-total_mass")
    const mass = document.getElementById("id_dispatch_note-mass")

    mass.value = (tMass.value / quantity.value).toFixed(0)

};

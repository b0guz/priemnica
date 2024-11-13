function SelectData() {
    let val = document.getElementById("id_supplier-id_supplier").value;

    let name_field = document.getElementById("id_supplier-name");
    let address_field = document.getElementById("id_supplier-address");

    let opts = document.getElementById('suppliers-list').children;
    for (let i = 0; i < opts.length; i++) {
      if (opts[i].value == val) {
        name_field.value = opts[i].getAttribute('data-name');
        address_field.value = opts[i].getAttribute('data-address');
        break;
      }
    }
  }
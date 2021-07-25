$(document).ready(() => {
  // On pag reload, Reset upsert form
  $('#serviceForm').trigger('reset');
  $('#images').val('');

  // Adding new row to price
  $('#addPriceRow').click(() => {
    $("#priceRows").append(`
      <div class="input-group mb-1">
        <input name="price_names[]" class="price-row form-control" type="text" placeholder="Name..."/>
        <span class="input-group-text" id="addon-wrapping"><i class="fas fa-dollar-sign"></i></span>
        <input name="price_values[]" class="price-row form-control" type="text" placeholder="Price..."/>
        <button type="button" class="price-del-row btn btn-danger"><i class="fas fa-trash"></i></button>
      </div>
    `);
  });

  // Deleting a price row
  $(document).on('click', '.price-del-row', (e) => {
    $(e.currentTarget).parent().remove();
  });
});

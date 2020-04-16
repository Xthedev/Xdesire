
  function payWithPaystack(){
    var handler = PaystackPop.setup({
      key: 'pk_live_acbc0a879d4df211c37fb6bc986afafe84340c17',
      email: sessionStorage.getItem('email'),
      amount: 20000,
      currency: "NGN",
      ref: ''+Math.floor((Math.random() * 1000000000) + 1), // generates a pseudo-unique reference. Please replace with a reference you generated. Or remove the line entirely so our API will generate one for you
      metadata: {
         custom_fields: [
            {
                display_name: "Mobile Number",
                variable_name: "mobile_number",
                value: sessionStorage.getItem('mobile')
            }
         ]
      },
      callback: function(response){
          alert('success. transaction ref is ' + response.reference);
          // $.post('/savepurchase',{
          //   email:session
          // })
          location.assign("{{ url_for('static', filename='books/') }}{{books.filename}}")
      },
      onClose: function(){
          alert('window closed');
      }
    });
    handler.openIframe();
  }


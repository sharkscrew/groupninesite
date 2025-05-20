setTimeout(() => {
   const successToastMessage = document.getElementById('toast-success');
   const errorToastMessage =document.getElementsById('toast-error');
   if (successToastMessage) {
       successToastMessage.style.display = 'none'
   }
   if (errorToastMessage) {
    errorToastMessage.style.display ='none'
   }
}, 3000);

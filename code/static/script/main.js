function confirm_cancel(message) {
    if(window.confirm(message)){
		return true;
	} else{
		window.alert('キャンセルされました');
		return false;
	}
}
(function() {
	$("#send").click(function() {
		$.post('/send/', {
			start: $("#start-address").val(),
			end: $("#end-address").val(),
		}).then(function(response) {
			var res = JSON.parse(response);
			var uber_info = "<thead><tr><th>Name</th><th>Price</ht></tr>";
			if (res.status == "success") {
				res.result.forEach(function(data) {
					text = "<tr>";
					text += "<td>" + data.display_name + "</td>";
					text += "<td>" + data.price + "</td>";
					text += "</tr>";
					uber_info += text;
				})
				uber_info += "</thead>";
				$("#result-text").html(uber_info);
			}
			else {
				$("#result-text").html("<span style='color:red'>Error</span>");
			}
			$("#result-text").show();

		})	
	})
})(jQuery)
function refreshJSON () {
    location.reload();
};

$.ajax({
	type: 'GET',
	url: '/listNotes',
	success: function(notes){
		var $notesInt = $('#notesInt');
		var $notesPlay = $('#notesPlay');
		for (var i = 0; i < notes.length; i++) {
			$notesInt.append('<option value="'+notes[i].id+'">'+notes[i].name+'</option>');
			$notesPlay.append('<option value="'+notes[i].id+'">'+notes[i].name+'</option>');
		};
	}
});

function MusicMenu () {
	id = document.getElementById("notesPlay").value;
	url1 = 'listSongFiles?id='+id;

	$.ajax({
		type: 'GET',
		url: url1,
		success: function(songs){
			var $songs= $('#songs');
			for (var i = 0; i < songs.length; i++) {
				$songs.append('<div data-role="collapsible" data-collapsed-icon="carat-d" data-expanded-icon="carat-u"><h4>'+songs[i].name+'</h4><audio controls><source src="http://localhost:8080/audio/1.wav" type="audio/wav"></audio></div>');
			};
		}
	});
}

function addNote() {
	var elem = document.getElementById("text");
	var nice = elem.value;
	var all = nice.replace(/"/g, "");
	var all = all.split(":");
	var name = all[0];
	var notas = all[1]+":"+all[2];
	var x = "name="+encodeURIComponent(name)+"&notes="+encodeURIComponent(notas);

	$.post("createSong",x,function(response){
		console.log(response);
		if(response == "Sucess"){
			document.getElementById("himynameis").innerHTML = "Musica enviada com sucesso!";
		}
		else{
			document.getElementById("himynameis").innerHTML = "Error!";
		}
	});
}

function addMusic () {
	var id = document.getElementById("notesInt").value;
	var registo = document.getElementById("registo").value;
	var efeito = document.getElementById("efeito").value;
	var nome = document.getElementById("nome").value;
	var x = "registration="+registo+"&id="+id+"&effects="+efeito+"&name=+"+nome;

	console.log(x);

	$.post("createInterpretation",x,function(response){
		if(response == "Sucess"){
			document.getElementById("himynameis2").innerHTML = "Musica enviada com sucesso!";
		}
		else{
			document.getElementById("himynameis2").innerHTML = "Error!";
		}
	});
}
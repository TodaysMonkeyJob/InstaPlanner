var cw = $('.profile-border').width();
$('.profile-border').css({'height': cw + 'px'});

document.querySelectorAll(".drop-zone__input").forEach((inputElement) => {
  const dropZoneElement = inputElement.closest(".drop-zone");

  dropZoneElement.addEventListener("click", (e) => {
    inputElement.click();

  });

  inputElement.addEventListener("change", (e) => {
    if (inputElement.files.length) {
      updateThumbnail(dropZoneElement, inputElement.files[0]);
    }
  });

  dropZoneElement.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZoneElement.classList.add("drop-zone--over");
  });

  ["dragleave", "dragend"].forEach((type) => {
    dropZoneElement.addEventListener(type, (e) => {
      dropZoneElement.classList.remove("drop-zone--over");
    });
  });

  dropZoneElement.addEventListener("drop", (e) => {
    e.preventDefault();

    if (e.dataTransfer.files.length) {
      inputElement.files = e.dataTransfer.files;
      updateThumbnail(dropZoneElement, e.dataTransfer.files[0]);
    }

    dropZoneElement.classList.remove("drop-zone--over");
  });
});

/**
 * Updates the thumbnail on a drop zone element.
 *
 * @param {HTMLElement} dropZoneElement
 * @param {File} file
 */
function updateThumbnail(dropZoneElement, file) {
  let thumbnailElement = dropZoneElement.querySelector(".drop-zone__thumb");

  // First time - remove the prompt
  if (dropZoneElement.querySelector(".drop-zone__prompt")) {
    dropZoneElement.querySelector(".drop-zone__prompt").remove();
  }

  // First time - there is no thumbnail element, so lets create it
  if (!thumbnailElement) {
    thumbnailElement = document.createElement("div");
    thumbnailElement.classList.add("drop-zone__thumb");
    dropZoneElement.appendChild(thumbnailElement);
  }

  thumbnailElement.dataset.label = file.name;

  // Show thumbnail for image files
  if (file.type.startsWith("image/")) {
    const reader = new FileReader();

    reader.readAsDataURL(file);
    reader.onload = () => {
      thumbnailElement.style.backgroundImage = `url('${reader.result}')`;
    };
  } else {
    thumbnailElement.style.backgroundImage = null;
  }
}
























exports.mount = function(dev, path, options, callback) {
  // See if there is already something mounted at the path
  var mountInfo = this.isMounted(path,false);
  if (mountInfo.mounted) {
    callback({"error": "Something is already mounted on " + path});
    return;
  }

  // See if the mountpoint exists.  If not, do we create?
  if (!fs.existsSync(path)) {
    if (options.createDir) {
      var mode = "0777";
      if (options.dirMode) {
        mode = options.dirMode;
      }
      fs.mkdirSync(path,mode);
    } else {
      callback({"error": "Mount directory does not exist"});
      return;
    }
  }
  // Make sure mountpoint is a directory
  if (!fs.statSync(path).isDirectory()) {
    callback({"error": "Mountpoint is not a directory"});
    return;
  }

  var qdev = this.quotePath(dev);
  var qpath = this.quotePath(path);
  // Build the command line
  var cmd = (options.noSudo?"":
      (options.sudoPath?options.sudoPath:"/usr/bin/sudo")+" ") +
      (options.mountPath?options.mountPath:"/bin/mount") + " " +
      (options.readonly?"-r ":"") +
      (options.fstype?"-t " + options.fstype + " ":"") +
      (options.fsopts?"-o " + options.fsopts + " ":"") +
      qdev + " " + qpath;

  // Let's do it!
  var mountProc = exec(cmd, function(error, stdout, stderr) {
    if (error !== null) {
      callback({ "error": "exec error " + error });
    } else {
      callback({ "OK": true });
    }
  });
}
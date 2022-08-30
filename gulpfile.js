const gulp = require("gulp");
const rename = require("gulp-rename");
const del = require("del");

gulp.task("compile-tailwind", function () {
  const postcss = require("gulp-postcss");
  return gulp
    .src("./src/index.css")
    .pipe(postcss([require("tailwindcss"), require("autoprefixer")]))
    .pipe(gulp.dest("src/assets/css/"))
    .pipe(rename("tailwind.css"));
});

gulp.task("rename-css", function () {
  return gulp
    .src("./src/assets/css/index.css")
    .pipe(rename("tailwind.css"))
    .pipe(gulp.dest("src/assets/css/"));
});

gulp.task("clean-css", function () {
  return del(["src/assets/css/index.css"]);
});

gulp.task("clean-pre-python-build", function () {
  console.log("Removing any pre-existing python folders and files before build...");

  console.log("Removing src/pyflaskdist/ ...");
  console.log("Removing build/ ...");
  console.log("Removing api.spec ...");

  return del(["src/pyflaskdist", "./api.spec", "./build"]);
});

gulp.task("clean-pre-electron-build", function () {
  console.log("Removing any pre-existing electron folders before build...");

  console.log("Removing dist_electron/ ...");

  return del(["./dist_electron"]);
});

gulp.task("copy-python", function () {
  console.log("Copying src/pyflask folder to dist_electron folder...");

  return gulp.src(["./src/pyflask/**/*"]).pipe(gulp.dest("./dist_electron/pyflask"));
});

gulp.task("copy-splash-screen", function () {
  console.log("Copying splash screen to dist_electron folder ...");

  return gulp.src(["./public/splash-screen.html"]).pipe(gulp.dest("./dist_electron"));
});

gulp.task("copy-app-icon", function () {
  console.log("Copying app icon to dist_electron folder ...");

  return gulp.src(["./src/assets/app-icons/Icon.png"]).pipe(gulp.dest("./dist_electron"));
});

gulp.task("build-css", gulp.series("compile-tailwind", "rename-css", "clean-css"));

gulp.task("copy-all", gulp.parallel("copy-python", "copy-splash-screen", "copy-app-icon"));

gulp.task("watch-dev", function () {
  gulp.watch("./src/index.css", gulp.series("build-css"));
  gulp.watch("./tailwind.config.js", gulp.series("build-css"));
  gulp.watch("./src/app.vue", gulp.series("build-css"));
  gulp.watch("./src/components/**/*", gulp.series("build-css"));
  gulp.watch("./src/views/**/*", gulp.series("build-css"));
  gulp.watch("./src/pyflask/**/*", gulp.series("copy-python"));
  gulp.watch("./src/splash-screen.html", gulp.series("copy-splash-screen"));
});

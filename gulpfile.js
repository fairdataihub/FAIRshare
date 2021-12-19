const gulp = require("gulp");
var rename = require("gulp-rename");
var del = require("del");

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

gulp.task("copy-python", function () {
  return gulp
    .src(["./src/pyflask/**/*"])
    .pipe(gulp.dest("./dist_electron/pyflask"));
});

gulp.task("copy-splash-screen", function () {
  return gulp
    .src(["./src/splash-screen.html"])
    .pipe(gulp.dest("./dist_electron"));
});

gulp.task(
  "build-css",
  gulp.series("compile-tailwind", "rename-css", "clean-css")
);

gulp.task("copy-all", gulp.parallel("copy-python", "copy-splash-screen"));

gulp.task("watch-dev", function () {
  gulp.watch("./src/index.css", gulp.series("build-css"));
  gulp.watch("./src/app.vue", gulp.series("build-css"));
  gulp.watch("./src/components/**/*", gulp.series("build-css"));
  gulp.watch("./src/views/**/*", gulp.series("build-css"));
  gulp.watch("./src/pyflask/**/*", gulp.series("copy-python"));
  gulp.watch("./src/splash-screen.html", gulp.series("copy-splash-screen"));
});

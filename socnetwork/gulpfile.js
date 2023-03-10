"use strict"

const {src, dest} = require("gulp")
const gulp = require("gulp")
const autoprefixer = require("gulp-autoprefixer");
const removeComments =  require('gulp-strip-css-comments');
const rigger = require("gulp-rigger");
const rename =  require("gulp-rename");
const sass =  require("gulp-sass")( require("sass"));
const plumber =  require("gulp-plumber");
const panini =  require("panini");
const del =  require("del");
const notify = require("gulp-notify");
const sourcemaps = require("gulp-sourcemaps");
const browserSync =  require("browser-sync").create();

/*Path*/
const srcPath = "src/"

const path = {
      build: {
          html: "templates/auth",
          html_workplace: "templates/profile",
          html_groupsettings: "templates/profile",
          css: "static/css/" ,
          js: "static/js/",
      },
      src: {
          html: srcPath + "*.html",
          html_workplace: srcPath + "user-workplace.html",
          html_groupsettings: srcPath + "settings-groups.html",
          css: srcPath + "assets/scss/*.scss",
          js: srcPath + "assets/js/*.js",
      },
      watch: {
          html: srcPath + "**/*.html",
          html_workplace: srcPath + "**/*.html",
          html_groupsettings: srcPath + "**/*.html",
          css: srcPath + "assets/scss/**/*.scss",
          js: srcPath + "assets/js/**/*.js",
      }
}

function serve() {
    browserSync.init({
        server: {
            baseDir: "./" + "templates/auth"
        }
    });
}

function html() {
    panini.refresh()
    return src(path.src.html, {base: srcPath})
        .pipe(plumber())
        .pipe(panini({root: srcPath, layouts: srcPath + "tpl/layouts/", partials: srcPath + "tpl/partials/"}))
        .pipe(dest(path.build.html))
        .pipe(browserSync.reload({stream:true}));
}

function html_workplace() {
    panini.refresh()
    return src(path.src.html_workplace, {base: srcPath})
        .pipe(plumber())
        .pipe(panini({root: srcPath, layouts: srcPath + "tpl/layouts/", partials: srcPath + "tpl/partials/"}))
        .pipe(dest(path.build.html_workplace))
        .pipe(browserSync.reload({stream:true}));
}

function html_groupsettings() {
    panini.refresh()
    return src(path.src.html_groupsettings, {base: srcPath})
        .pipe(plumber())
        .pipe(panini({root: srcPath, layouts: srcPath + "tpl/layouts/", partials: srcPath + "tpl/partials/"}))
        .pipe(dest(path.build.html_groupsettings))
        .pipe(browserSync.reload({stream:true}));
}

function css() {
    return src(path.src.css, {base: srcPath + "assets/scss/"})

        .pipe(sourcemaps.init())
        .pipe(plumber({
            errorHandler : function(err) {
                notify.onError({
                    title:     "SCSS Error",
                    message:   "Error: <%= error.message %>"
                })(err)
                this.emit('end');
            }
        }))
        .pipe(sass())
        .pipe(autoprefixer())
        .pipe(dest(path.build.css))
        .pipe(removeComments())
        .pipe(rename({
            suffix: ".min",
            extname: ".css"
        }))
        .pipe(sourcemaps.write())
        .pipe(dest(path.build.css))
        .pipe(browserSync.reload({stream:true}));
}

function js() {
    return src(path.src.js, {base: srcPath + "assets/js/"})
        .pipe(plumber({
            errorHandler : function(err) {
                notify.onError({
                    title:     "JS Error",
                    message:   "Error: <%= error.message %>"
                })(err)
                this.emit('end');
            }
        }))
        .pipe(rigger())
        .pipe(dest(path.build.js))
        .pipe(rename({
            suffix: ".min",
            extname: ".js"

        }))
        .pipe(dest(path.build.js))
        .pipe(browserSync.reload({stream:true}));

}

function watchFiles() {
    gulp.watch([path.watch.html], html)
    gulp.watch([path.watch.html_workplace], html_workplace)
    gulp.watch([path.watch.html_groupsettings], html_groupsettings)
    gulp.watch([path.watch.css], css)
    gulp.watch([path.watch.js], js)
}

const build = gulp.series(gulp.parallel(html, html_workplace, html_groupsettings, css, js))
const watch = gulp.parallel(build, watchFiles, serve)


exports.html = html
exports.html_workplace = html_workplace
exports.html_groupsettings = html_groupsettings
exports.css = css
exports.js = js
exports.build = build
exports.watch = watch
exports.default = watch

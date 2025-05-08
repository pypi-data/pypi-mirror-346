
PACKAGE_JSON = {
	"name": "{name}",
	"version": "1.0.0",
	"description": "{description}",
	"main": "main.js",
	"scripts": {
		"dev": "node esbuild.config.mjs",
		"test": "obs-dev plugin test",
		"build": "tsc -noEmit -skipLibCheck && node esbuild.config.mjs production",
	},
	"keywords": [],
	"author": "",
	"license": "MIT",
	"devDependencies": {
		"@types/node": "^16.11.6",
		"@typescript-eslint/eslint-plugin": "5.29.0",
		"@typescript-eslint/parser": "5.29.0",
		"builtin-modules": "3.3.0",
		"esbuild": "^0.25.1",
		"obsidian": "latest",
		"tslib": "2.4.0",
		"typescript": "4.7.4"
	}
}

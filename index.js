/**
 * This file will be more useful in the future.
 * For now only look at ./main.py
 */

import fetch from 'node-fetch';
import { parseString } from 'xml2js';

const URL = 'https://github-readme-stats.vercel.app/api/top-langs/?username=';

async function user_exists(username) {
  const resp = await fetch(`https://api.github.com/users/${username}`);
  return resp;
}

async function get_svg(username) {
  const resp = await fetch(`${URL}${username}`);
  const body = await resp.text();
  return body;
}

function main(argv) {
  argv = argv.splice(2, argv.length);
  if (argv.length != 1) {
    console.error('ERROR: Provide a github username.\nRun: `node ./index.js Zielin0`');
    process.exit(1);
  }
  const username = argv[0];

  user_exists(username).then(data => {
    const status = data.ok;
    if (!status) {
      console.error(`ERROR: User '${username}' doesn't exist.`);
      process.exit(1);
    }
  });

  get_svg(username).then(data => {
    parseString(data, (err, res) => {
      const langs = res['svg']['g'][1]['svg'][0]['g'];

      console.log(`${username}'s Top Languages:`);

      let n = 0;

      for (let lang of langs) {
        n++;
        const langName = lang['text'][0]['_'];
        const langPercent = lang['text'][1]['_'];
        console.log(`${n}. ${langName} ${langPercent}`);
      }
    });
  });
}

main(process.argv);

// Commit message rules of rules/workflow/committing.md: a Conventional Commits 1.0.0 header of at
// most 72 characters on every commit, a local merge commit included, and no AI attribution trailer
// or marker. Text below Git's scissors line is the verbose diff, not the message.
const TRAILER = /^\s*(Co-Authored-By|Signed-off-by|Claude-Session)\s*:/im;
const AI_MARK = /Generated with \[Claude Code\]|noreply@anthropic\.com|claude\.ai\/code\/session/i;
const SCISSORS = /^# -+ >8 -+$/m;

const noAttribution = ({ raw }) => {
  const message = raw.split(SCISSORS)[0];
  return [!(TRAILER.test(message) || AI_MARK.test(message)), "remove the AI attribution trailer or marker"];
};

// A merge Git itself names (a pull request, a remote-tracking branch, a tag, a pull from a remote)
// and a revert or fixup keep their generated subject; a local merge of a commit or a branch does not.
const GENERATED = /^(Revert |fixup! |squash! |amend! |Merge pull request |Merge remote-tracking branch |Merge tag |Merge branch '[^']*' of )/;

export default {
  defaultIgnores: false,
  ignores: [(message) => GENERATED.test(message)],
  parserPreset: {
    parserOpts: {
      headerPattern: /^([a-z]+)(?:\(([^)]+)\))?!?: (\S.*)$/,
      headerCorrespondence: ["type", "scope", "subject"],
    },
  },
  plugins: [{ rules: { "no-attribution": noAttribution } }],
  rules: {
    "header-max-length": [2, "always", 72],
    "type-empty": [2, "never"],
    "subject-empty": [2, "never"],
    "no-attribution": [2, "always"],
  },
};
